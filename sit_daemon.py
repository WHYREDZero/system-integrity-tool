from sit_core import *
from threading import *
import time
import sys
try:
    hashDBName = sys.argv[1]
except:
    hashDBName = input('Enter Hash DB Name: ')


def Scan(hashDBName):
    while True:
        scanTrackedFilesWorkflow(hashDBName)
        time.sleep(60)


T = Thread(target=Scan(hashDBName),daemon=True)
T.start()