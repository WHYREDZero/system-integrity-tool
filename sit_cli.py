from sit_core import *
import sys


def printHelp():
    print("System Integrity Tool Help:")
    print("Format: python sit_cli.py [COMMAND] [OBJECTS]")
    print("Commands:")
    print("t: Track new files for Integrity Check, takes Hash DB Name and File or Folder path")
    print("s: Scan tracked files for Integrity Check, takes Hash DB Name")
    print("r: Retrack files for Integrity Check, takes Hash DB Name and File or Folder path")
    print("b: Restore modified files from backup, takes Hash DB Name and File or Folder path")


try:
    option = sys.argv[1]
    if option == 't':
        hashDBName = sys.argv[2]
        paths = sys.argv[3]
        trackNewFilesWorkflow(hashDBName, paths)
    elif option == 's':
        hashDBName = sys.argv[2]
        scanTrackedFilesWorkflow(hashDBName)
    elif option == 'r':
        hashDBName = sys.argv[2]
        paths = sys.argv[3]
        retrackFilesWorkflow(hashDBName, paths)
    elif option == 'b':
        hashDBName = sys.argv[2]
        paths = sys.argv[3]
        restoreModifiedFilesWorkflow(hashDBName, paths)
    else:
        printHelp()
except:
    printHelp()