#!/usr/bin/env python
from pathlib import Path
import xattr
import subprocess

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder


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
    # seems to not need sudo?  not sure why?

    deflagCmd = ['/usr/bin/xattr', '-rd', QUARANTINE_KEY, str(plugPath)]

    pout2 = subprocess.run(deflagCmd, capture_output=True)
 
    return pout2.returncode 


def deFlagPluginList(plugsToDeflag):
    resultList = []
    for plug in plugsToDeflag:
        thisResult = deflagOnePlugin(plug)
        resultList.append([plugsToDeflag, thisResult])
    return resultList


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in getQuarFlaggedPluginList()]

class PlugDeQuar(App):
    def build(self):
 
        f = FloatLayout()
        r = RV()
        r.size_hint = (1,0.9)
        print(dir(r))
        f.add_widget(r)
        return f
    

if __name__ == "__main__":

    PlugDeQuar().run()

