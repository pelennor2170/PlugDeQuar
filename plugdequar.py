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

    def update(self, newFlaggedList):
        self.data = []
        self.data = [{'text': str(x)} for x in newFlaggedList]

class PlugDeQuar(App):
    def __init__(self, **kwargs):
        super(PlugDeQuar, self).__init__(**kwargs)
        self.quarPlugList = getQuarFlaggedPluginList()

    def build(self):
 
        f = FloatLayout()
        r = RV()
        r.size_hint = (1,0.9)
        r.update(self.quarPlugList)
        f.add_widget(r)

        btn = Button(text = 'De-quarantine all...', 
                            size_hint = (0.2, 0.1), 
                            pos_hint = {'center_x' : 0.5 ,'y': 0.9},
                            background_normal = '',
                            background_color = (0,0,1,1)
        )

        btn.bind(on_press=self.dequarPressed)
        f.add_widget(btn)

        self.RV = r
        self.layout = f
        return f

    def dequarPressed(self, someArg):
        if len(self.quarPlugList) > 0:

            resultList = deFlagPluginList(self.quarPlugList)
            #print(resultList)
            self.quarPlugList = getQuarFlaggedPluginList()
            self.RV.update(self.quarPlugList)

            if len(self.quarPlugList) == 0:
                print('Successfully de-quarantined all files')
                lblText = 'Successfully de-quarantined all files'
                lbl = Label(text='Successfully de-quarantined all files!')

            else :
                lblText='Error de-quarantining one or more files'
                print('Error de-quarantining one or more files!')

            lbl = Label(text=lblText) 
            self.layout.add_widget(lbl)


    

if __name__ == "__main__":

    PlugDeQuar().run()

