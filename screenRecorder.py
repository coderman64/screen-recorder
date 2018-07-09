"""
    ScreenRecorder.py is a small, Windows app that records video from your screen and audio from the default microphone
    Copyright (C) 2018  coderman64

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

import subprocess
from tkinter import *
from time import sleep
import os
import recordFile, Webcam

class Alert(Toplevel):
    
    def __init__(self, parent):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        self.parent = parent

        self.result = None

        self.OK = Button(self, text = "OK", width=10, command = self.ok, default=ACTIVE)
        self.OK.pack()
        self.bind("<Return>", self.test)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.wait_window(self)
    def test(self):
        pass

class App: #the main class for the main window
    def __init__(self, master):
        
        label1 = Label(master, text="File Name:")
        label1.grid(row = 0, column = 0, sticky = "")
        self.entry1 = Entry(master)
        self.entry1.grid(row = 0, column = 1)
        defaultFile = "ScreenCapture.mp4"
        available = False
        fileNum = 0
        try:
            os.mkdir("ScreenCaptures")
        except FileExistsError:
            pass
        os.chdir("ScreenCaptures")
        while available == False:
            matches = 0
            for item in os.listdir():
                if item == defaultFile:
                    matches += 1
            if matches == 0:
                available = True
            else:
                fileNum += 1
                defaultFile = "ScreenCapture"+str(fileNum)+".mp4"
        os.chdir("..")
        self.entry1.insert(END,defaultFile)
        master.title(string = "Screen Recorder")
        master.iconbitmap("icon.ico")
        master.resizable(width = False, height = False)

        self.what = "desktop"
        self.radio2 = Radiobutton(master, text="record the window with the title of: ", variable=self.what, value = "title", command = self.enDis1)
        self.radio1 = Radiobutton(master, text="record the entire desktop", variable=self.what, value = "desktop", command = self.enDis)
        self.radio1.select()
        self.radio2.deselect()
        self.radio1.grid(row = 1, column = 0, sticky="w")
        self.radio2.grid(row = 2, column = 0, sticky = "w")
        self.entry2 = Entry(master, state=DISABLED)
        self.entry2.grid(row = 2, column = 1)

        self.webcamdevices = Webcam.listCam()
        
        self.webcamrecorder = Webcam.capturer("")
        
        self.rcchecked = False
        self.recordcam = Checkbutton(master, text="Record from webcam", command = self.checkboxChanged)
        self.recordcam.grid(row = 3, column = 0)

        self.devicename = StringVar(master)
        self.devicename.set(self.webcamdevices[0])
        self.deviceselector = OptionMenu(master, self.devicename, *self.webcamdevices)
        self.deviceselector.config(state=DISABLED)
        self.deviceselector.grid(row = 3, column = 1)
        
        self.startButton = Button(master, text="Start Recording", command = self.startRecord)
        self.startButton.grid(row = 4, column = 0, columnspan = 2)

        self.recording = False
        self.proc = None
        self.recorder = recordFile.recorder()
        self.master = master
        self.mergeProcess = None
        self.pollClosed()

    def pollClosed(self):
        if self.recording == True:
            if self.proc.poll() != None:
                print("Something exploded!")
                self.startRecord()
        if self.mergeProcess and self.recording == False:
            if self.mergeProcess.poll() != None:
                self.startButton.config(text="Start Recording", state = NORMAL)
                self.master.title(string = "Screen Recorder")
        root.after(100, self.pollClosed)

    def enDis(self):
        self.entry2.config(state=DISABLED)
        self.what = "desktop"
    def enDis1(self):
        self.entry2.config(state = NORMAL)
        self.what = "title"
    def checkboxChanged(self):
        self.rcchecked = not self.rcchecked
        #print("Checkbox changed to " + str(self.rcchecked))
        if self.rcchecked:
            self.deviceselector.config(state = NORMAL)
        else:
            self.deviceselector.config(state = DISABLED)
    def startRecord(self):
        if self.recording == False:
            self.startButton.config(text="Stop Recording")
            self.filename = self.entry1.get()
            self.entry1.config(state = DISABLED)
            self.radio1.config(state = DISABLED)
            self.radio2.config(state = DISABLED)
            self.deviceselector.config(state = DISABLED)
            self.master.title(string = "Screen Recorder (Recording...)")
            try:
                os.mkdir("tmp")
            except FileExistsError:
                pass
            if self.what == "title":
                self.entry2.config(state = DISABLED)
            self.recording = True
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            if self.what == "title":
                self.proc = subprocess.Popen(args=['ffmpeg.exe','-f','gdigrab','-i',str("title="+self.entry2.get()),'-framerate','30','-y','-c:v','mpeg4','-qscale:v','7','tmp/tmp.mkv'], startupinfo=startupinfo)
            else:
                self.proc = subprocess.Popen(args=['ffmpeg.exe','-f','gdigrab','-i',"desktop",'-framerate','30','-y','-c:v','mpeg4','-qscale:v','7','tmp/tmp.mkv'], startupinfo=startupinfo)
            self.recorder.record("tmp/tmp.wav")
            self.recordcam.config(state = DISABLED)
            if self.rcchecked == True:
                self.webcamrecorder.setDevice(str(self.devicename.get()))
                self.webcamrecorder.startCapture("tmp/webcamtmp.mkv")
            root.grab_set()
        elif self.recording == True:
            defaultFile = self.filename
            self.entry1.config(state = NORMAL)
            self.radio1.config(state = NORMAL)
            self.radio2.config(state = NORMAL)
            self.recordcam.config(state = NORMAL)
            self.deviceselector.config(state = NORMAL)
            if self.what == "title":
                self.entry2.config(state = NORMAL)
            available = False
            fileNum = 0
            self.recording = False
            self.proc.terminate()
            self.recorder.stop_recording()
            if self.rcchecked:
                self.webcamrecorder.stopCapture()
            try:
                os.mkdir("ScreenCaptures")
            except FileExistsError:
                pass
            self.master.title(string = "Screen Recorder (converting...)")
            self.startButton.config(text="converting your previous recording, please wait...", state = DISABLED)
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            if self.rcchecked:
                self.mergeProcess = subprocess.Popen(args= ["ffmpeg","-i",'tmp/tmp.mkv','-i','tmp/tmp.wav','-i','tmp/webcamtmp.mkv','-filter_complex','[2:v] scale=640:-1 [inner]; [0:0][inner] overlay=0:0 [out]',"-shortest",'-map','[out]','-y',"ScreenCaptures/"+self.filename])
            else:
                self.mergeProcess = subprocess.Popen(args= ["ffmpeg","-i",'tmp/tmp.mkv','-i','tmp/tmp.wav',"-shortest",'-y',"ScreenCaptures/"+self.filename], startupinfo=startupinfo)


            os.chdir("ScreenCaptures")
            while available == False:
                matches = 0
                for item in os.listdir():
                    if item == defaultFile:
                        matches += 1
                if matches == 0:
                    available = True
                else:
                    fileNum += 1
                    file = self.filename.split(".")
                    defaultFile = file[0].rstrip("1234567890")+str(fileNum)+"."+file[1]
                self.entry1.delete(0,END)
                self.entry1.insert(END,defaultFile)
            os.chdir("../")
            
root = Tk()

app = App(root)
root.mainloop()

