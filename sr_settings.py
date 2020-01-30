"""
cmdGen.py generates ffmpeg commands to record your screen
Copyright (C) 2020  coderman64

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from tkinter import *
from tkinter.ttk import Notebook, Button, Radiobutton, Checkbutton
from cmdGen import cmdGen

class settingsWin(Toplevel):
    def __init__(self, parent,sourceCmdGen,audioRec):
        Toplevel.__init__(self, parent)
        #self.transient(parent)
        self.cmdGen = sourceCmdGen
        self.audioRec = audioRec

        self.title(string = "Screen Recorder - Settings")
        self.iconbitmap("icon.ico")
        self.resizable(width = False, height = False)
        self.minsize(400,450)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.notebook = Notebook(self)
        self.notebook.grid(row=0,column=0,columnspan=4,sticky="nesw",padx=5,pady=5)

        ########################################### VIDEO OPTIONS ##############################################      
        self.videoOptions = Frame(self)
        self.videoOptions.columnconfigure(1,weight=1)

        Label(self.videoOptions,text="Suggested FPS (Not guaranteed): ").grid(row=0,column=0)

        self.FPSVar = StringVar()
        self.FPSspin = Spinbox(self.videoOptions,from_=1,to=120,textvariable=self.FPSVar)
        self.FPSspin.grid(row=0,column=1,sticky="ew",pady=5)
        self.FPSVar.set(self.cmdGen.fps)

        self.hwaccVar = StringVar()

        Label(self.videoOptions,text="Encoding (GPU encoding may improve perfomance):").grid(row=1,column=0,columnspan=2,sticky="w")
        self.buttonCPU = Radiobutton(self.videoOptions,text="CPU-only encoder (all formats)",variable=self.hwaccVar,value="CPU")
        self.buttonCPU.grid(row=2,column=0,columnspan=2,sticky="w")
        self.buttonNVENC = Radiobutton(self.videoOptions,text="Nvidia NVENC GPU encoder (h.264 only)",variable=self.hwaccVar,value="NVENC")
        self.buttonNVENC.grid(row=3,column=0,columnspan=2,sticky="w")
        
        if self.cmdGen.encoder == "mpeg4":
            self.hwaccVar.set("CPU")
        elif self.cmdGen.encoder == "h264_nvenc":
            self.hwaccVar.set("NVENC")
        
        self.drawMouseVar = IntVar()
        self.drawMouseVar.set(self.cmdGen.drawMouse)
        self.drawMouseCheck = Checkbutton(self.videoOptions,text="Draw mouse",variable=self.drawMouseVar)
        self.drawMouseCheck.grid(row=5,column=0,columnspan=2,sticky='w',pady=10)

        self.notebook.add(self.videoOptions,text="Video Options")

        ######################################################################################################################
        ############################################### AUDIO OPTIONS #####################################################
        self.audioOptions = Frame(self)
        self.audioOptions.columnconfigure(0,weight=1)
        self.audioOptions.rowconfigure(2,weight=1)

        self.audInputVar = StringVar()

        self.defaultCheck = Radiobutton(self.audioOptions,text="Record from the default device only",value="default",variable = self.audInputVar)
        self.defaultCheck.grid(row=0,column=0,sticky="w")

        self.selectedCheck = Radiobutton(self.audioOptions,text="Record from these devices:", value="selected",variable=self.audInputVar)
        self.selectedCheck.grid(row=1,column=0,sticky="w")

        self.audioDevices = Listbox(self.audioOptions,selectmode="multiple")
        self.audioDevices.grid(row=2,column=0,sticky='news')

        self.deviceIDList = []
        for i in range(self.audioRec.getDeviceCount()):
            if self.audioRec.isInputDevice(i):
                self.deviceIDList.append(i)
                self.audioDevices.insert("end",self.audioRec.getAPIName(i)+" || "+self.audioRec.getDeviceName(i))
                if i in self.audioRec.devices:
                    self.audioDevices.selection_set('end')

        self.audInputVar.trace("w",self.audButtonChange)
        if self.audioRec.devices == [None]:
            self.audInputVar.set("default")
        else:
            self.audInputVar.set("selected")
        
        self.notebook.add(self.audioOptions,text="Audio Options")

        ####################################################################################################################

        self.okButton = Button(self,text="OK",width=9,command=self.applyQuit)
        self.okButton.grid(row=1,column=1,padx=4,pady=4)

        self.cancelButton = Button(self,text="Cancel",width=9,command=self.destroy)
        self.cancelButton.grid(row=1,column=2,padx=4,pady=4)

        self.applyButton = Button(self,text="Apply",width=9,command=self.apply)
        self.applyButton.grid(row=1,column=3,padx=4,pady=4)

        self.grab_set()
        self.focus()
    def audButtonChange(self,*args):
        if self.audInputVar.get() == "default":
            self.audioDevices.config(state=DISABLED)
        else:
            self.audioDevices.config(state=NORMAL)
    def apply(self):
        self.cmdGen.config(fps=int(self.FPSVar.get()))
        if self.hwaccVar.get() == "CPU":
            self.cmdGen.config(encoder='mpeg4',hwaccel=None)
        elif self.hwaccVar.get() == "NVENC":
            self.cmdGen.config(encoder='h264_nvenc',hwaccel=None)
        if self.audInputVar == "default":
            self.audioRec.setToDefault()
        else:
            deviceList = []
            for i in range(len(self.deviceIDList)):
                if self.audioDevices.selection_includes(i):
                    deviceList.append(self.deviceIDList[i])
            print("AUD DEV LIST: "+str(deviceList))
            self.audioRec.setToDevices(deviceList)
    def applyQuit(self):
        self.apply()
        self.destroy()

if __name__ == "__main__":
    test = Tk()
    phil = settingsWin(test)
    test.mainloop()