from sit_core import *
import PySimpleGUI as sg


def TNFWindow(hashDBName):
    event, values = sg.Window('Track New Files', [[sg.Text('File or Folder name')], [
                              sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()]]).read(close=True)
    paths = values[0]
    trackNewFilesWorkflow(hashDBName, paths)


def STFWindow(hashDBName):
    event, values = sg.Window('Scan Tracked Files', [[sg.Text(
        'Please check notifications for modified files.')], [sg.OK()]]).read(close=True)
    scanTrackedFilesWorkflow(hashDBName)


def RTFWindow(hashDBName):
    event, values = sg.Window('Re-Track Files', [[sg.Text('File or Folder name')], [
                              sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()]]).read(close=True)
    paths = values[0]
    retrackFilesWorkflow(hashDBName, paths)


def RMFWindow(hashDBName):
    event, values = sg.Window('Restore Modified Files', [[sg.Text('File or Folder name')], [
                              sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()]]).read(close=True)
    paths = values[0]
    restoreModifiedFilesWorkflow(hashDBName, paths)


layout = [[sg.Text('Enter hash database name and select one option.'), sg.InputText()],
          [sg.OptionMenu(values=('Track New Files',
                         'Scan Tracked Files', 'Re-Track Files', 'Restore Modified Files'))],
          [sg.Button('Ok'), sg.Button('Cancel')]]

window = sg.Window('System Integrity Tool', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    hashDBName = values[0]
    if values[1] == 'Track New Files':
        TNFWindow(hashDBName)
    elif values[1] == 'Scan Tracked Files':
        STFWindow(hashDBName)
    elif values[1] == 'Re-Track Files':
        RTFWindow(hashDBName)
    elif values[1] == 'Restore Modified Files':
        RMFWindow(hashDBName)

window.close()
