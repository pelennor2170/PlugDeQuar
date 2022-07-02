#!/usr/bin/env python
from pathlib import Path
import xattr

QUARANTINE_KEY = 'com.apple.quarantine'

PLUGIN_GLOB_LIST = ['*.vst', '*.vst3', '*.component']


def getPluginBaseFolders():
    pbf = [Path('/Library/Audio/Plug-Ins')]

    ppf = Path('~/Library/Audio/Plug-Ins').expanduser()
    if ppf.exists():
        pbf.append(ppf)
    
    return pbf

def getQuarFlaggedPluginList():
    qfpl = []

    for fold in getPluginBaseFolders():
        for tg in PLUGIN_GLOB_LIST:
            for i in fold.rglob(tg):
                xa = xattr.xattr(i)
                try:
                    if QUARANTINE_KEY in xa.keys():
                        qfpl.append(i)
                except:
                    pass
    return qfpl


def deflagOnePlugin(plugPath):
    # this needs to call xattr -rd on the path

    return 0 # success


def deFlagPluginList(plugsToDeflag):
    resultList = []
    for plug in plugsToDeflag:
        thisResult = deflagOnePlugin(plug)
        resultList.append(thisResult)
    return resultList

qfl = getQuarFlaggedPluginList()

print(deFlagPluginList(qfl))

#for f in [i for i in baseDir.iterdir() if i.is_file()] :
#    print(f)

# for d in [i for i in baseDir.rglob('*')]:
#     xa = xattr.xattr(d)
#     try:
#         if QUARANTINE_KEY in xa.keys():
#             try:
#                 del xa[QUARANTINE_KEY]
#             except:
#                 print('uh oh')
#             print(d)
#     except:
#         print('spagetti-oh')
#         print(d)
