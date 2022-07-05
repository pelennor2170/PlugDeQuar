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


Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(40)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


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

#qfl = getQuarFlaggedPluginList()

#print(deFlagPluginList(qfl))

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        flaggedPlugs = getQuarFlaggedPluginList()
        self.data = [{'text' : str(item) } for item in flaggedPlugs]
        print(self.data)



class PlugDeQuar(App):
    def build(self):
        f=FloatLayout()
        # s=Scatter()
        # l=Label(text='Hello', font_size=150)
        r = RV(size_hint = (1,0.9),pos_hint = {"x":0, "y":0})
        f.add_widget(r)
        b = Button(text = 'Dequarantine all...', pos_hint = {"x":0.5, "top":1}, size_hint = (0.5, 0.1))
        f.add_widget(b)
        # s.add_widget(l)
        #popup = Popup(title='Please wait...',
        #content=Label(text='Scanning plugin folders'),
        #size_hint=(None, None), size=(400, 400))
        return f
    

if __name__ == "__main__":

    #flaggedPlugins = getQuarFlaggedPluginList()
    #print(flaggedPlugins)
    PlugDeQuar().run()

