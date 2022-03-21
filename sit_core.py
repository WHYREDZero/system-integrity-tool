import os
import hashlib
import sqlite3
from pathlib import Path
import shutil
from plyer import notification

# Core functions begin here


def parseFiles(pathName):
    fileList = []
    rawPathName = r'{}'.format(pathName)
    if(os.path.isfile(rawPathName)):
        fileList.append(rawPathName)
        return fileList
    for subDir, dirs, files in os.walk(rawPathName):
        for fileName in files:
            filePath = subDir + os.sep + fileName
            fileList.append(filePath)
    return fileList


def getFileHash(filePath):
    hashObject = hashlib.sha512()
    try:
        with open(filePath, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                hashObject.update(chunk)
    except Exception as e:
        return e
    return hashObject.hexdigest()


def isModified(filePath, oldHash):
    if getFileHash(filePath) != oldHash:
        return True
    else:
        return False


def hashDBInit(hashDBName):
    connectionToDB = sqlite3.connect(hashDBName)
    cursorObject = connectionToDB.cursor()
    try:
        cursorObject.execute(
            'CREATE TABLE IF NOT EXISTS hashes ([fileName] TEXT PRIMARY KEY, [hashValue] TEXT, [isModified] TEXT)')
        connectionToDB.commit()
        connectionToDB.close()
    except Exception as e:
        print(e)


def storeHashToDB(hashDBName, fileName, hashValue, isModified="False"):
    connectionToDB = sqlite3.connect(hashDBName)
    cursorObject = connectionToDB.cursor()
    try:
        cursorObject.execute(
            "INSERT INTO hashes VALUES (?, ?, ?)", (fileName, hashValue, isModified))
        connectionToDB.commit()
        connectionToDB.close()
    except Exception as e:
        print(e)


def getHashFromDB(hashDBName, fileName):
    connectionToDB = sqlite3.connect(hashDBName)
    cursorObject = connectionToDB.cursor()
    try:
        for row in cursorObject.execute(
                "SELECT hashValue FROM hashes WHERE fileName=:name", {"name": fileName}):
            connectionToDB.commit()
            connectionToDB.close()
            return row[0]
    except Exception as e:
        return e


def updateHashInDB(hashDBName, fileName, hashValue, isModified="True"):
    connectionToDB = sqlite3.connect(hashDBName)
    cursorObject = connectionToDB.cursor()
    try:
        cursorObject.execute(
            "UPDATE hashes SET hashValue=:newHash, isModified=:modified WHERE fileName=:file", {"file": fileName, "newHash": hashValue, "modified": isModified})
        connectionToDB.commit()
        connectionToDB.close()
    except Exception as e:
        print(e)


def getFileListFromDB(hashDBName):
    connectionToDB = sqlite3.connect(hashDBName)
    cursorObject = connectionToDB.cursor()
    try:
        fileList = []
        for row in cursorObject.execute("SELECT fileName FROM hashes"):
            fileList.append(row[0])
        connectionToDB.commit()
        connectionToDB.close()
        return fileList
    except Exception as e:
        return e


def getModifiedListFromDB(hashDBName):
    connectionToDB = sqlite3.connect(hashDBName)
    cursorObject = connectionToDB.cursor()
    try:
        fileList = []
        for row in cursorObject.execute("SELECT fileName FROM hashes WHERE isModified=\'True\'"):
            fileList.append(row[0])
        connectionToDB.commit()
        connectionToDB.close()
        return fileList
    except Exception as e:
        return e


# Core functions end here


# Extra functions begin here


def createBackup(fileName):
    filePath = Path(fileName)
    backupPath = filePath.with_suffix('.bak')
    shutil.copy(filePath, backupPath)


def restoreBackup(fileName):
    filePath = Path(fileName)
    backupPath = filePath.with_suffix('.bak')
    shutil.copy(backupPath, filePath)


def sendNotification(notificationMessage, notificationTitle="System Integrity Tool"):
    notification.notify(
        title=notificationTitle,
        message=notificationMessage
    )


def removeDuplicates(inputList):
    outputList = []
    for element in inputList:
        if element not in outputList:
            outputList.append(element)
    outputList.sort()
    return outputList


def returnAsList(inputObject):
    outputList = []
    if isinstance(inputObject, list):
        outputList = inputObject
    else:
        outputList.append(inputObject)
    return outputList
# Extra functions end here

# Generalized workflows begin here


def trackNewFilesWorkflow(hashDBName, paths):
    hashDBInit(hashDBName)
    pathList = returnAsList(paths)
    filesToTrack = []
    for path in pathList:
        filesToTrack.extend(parseFiles(path))
    filesToTrack = removeDuplicates(filesToTrack)
    for file in filesToTrack:
        hashValue = getFileHash(file)
        storeHashToDB(hashDBName, file, hashValue)
        createBackup(file)


def retrackFilesWorkflow(hashDBName, paths):
    hashDBInit(hashDBName)
    pathList = returnAsList(paths)
    filesToTrack = []
    for path in pathList:
        filesToTrack.extend(parseFiles(path))
    filesToTrack = removeDuplicates(filesToTrack)
    for file in filesToTrack:
        hashValue = getFileHash(file)
        updateHashInDB(hashDBName, file, hashValue, isModified="False")
        createBackup(file)


def scanTrackedFilesWorkflow(hashDBName):
    fileList = getFileListFromDB(hashDBName)
    for file in fileList:
        oldHash = getHashFromDB(hashDBName, file)
        if isModified(file, oldHash):
            updateHashInDB(hashDBName, file, getFileHash(file))
    modifiedFiles = getModifiedListFromDB(hashDBName)
    for file in modifiedFiles:
        message = file + " was modified!"
        print(message)
        sendNotification(message)


def restoreModifiedFilesWorkflow(hashDBName, file):
    fileList = getFileListFromDB(hashDBName)
    for file in fileList:
        oldHash = getHashFromDB(hashDBName, file)
        if isModified(file, oldHash):
            updateHashInDB(hashDBName, file, getFileHash(file))
    modifiedFiles = getModifiedListFromDB(hashDBName)
    for file in modifiedFiles:
        restoreBackup(file)
        hashValue = getFileHash(file)
        updateHashInDB(hashDBName, file, hashValue, isModified="False")
# Generalized workflows end here
