from tkinter import *
from tkinter.ttk import Notebook, Button, Radiobutton, Checkbutton
from cmdGen import cmdGen

print("HAS IMPORT")

class settingsWin(Toplevel):
    def __init__(self, parent,sourceCmdGen):
        print("AH")
        print(parent)
        Toplevel.__init__(self, parent)
        #self.transient(parent)
        self.cmdGen = sourceCmdGen

        self.title(string = "Screen Recorder - Settings")
        self.iconbitmap("icon.ico")
        self.resizable(width = False, height = False)
        self.minsize(400,450)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.notebook = Notebook(self)
        self.notebook.grid(row=0,column=0,columnspan=4,sticky="nesw",padx=5,pady=5)

        self.genFrame = Frame(self)
        Label(self.genFrame,text="FPS: ").grid(row=0,column=0)

        self.FPSVar = StringVar()
        self.FPSspin = Spinbox(self.genFrame,from_=1,to=120,textvariable=self.FPSVar)
        self.FPSspin.grid(row=0,column=1,sticky="ew")
        self.FPSVar.set(self.cmdGen.fps)

        self.notebook.insert("end",self.genFrame,text="General")

        self.hwaccVar = StringVar()
        
        self.videoOptions = Frame(self)
        Label(self.videoOptions,text="Encoding (GPU encoding may improve perfomance):").grid(row=0,column=0,sticky="w")
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

        self.notebook.insert("end",self.videoOptions,text="Video Options")

        self.okButton = Button(self,text="OK",width=9,command=self.applyQuit)
        self.okButton.grid(row=1,column=1,padx=4,pady=4)

        self.cancelButton = Button(self,text="Cancel",width=9,command=self.destroy)
        self.cancelButton.grid(row=1,column=2,padx=4,pady=4)

        self.applyButton = Button(self,text="Apply",width=9,command=self.apply)
        self.applyButton.grid(row=1,column=3,padx=4,pady=4)

        self.grab_set()
        self.focus()
    def apply(self):
        self.cmdGen.config(fps=int(self.FPSVar.get()))
        if self.hwaccVar.get() == "CPU":
            self.cmdGen.config(encoder='mpeg4',hwaccel=None)
        elif self.hwaccVar.get() == "NVENC":
            self.cmdGen.config(encoder='h264_nvenc',hwaccel=None)
    def applyQuit(self):
        self.apply()
        self.destroy()

if __name__ == "__main__":
    print("TIKES")
    test = Tk()
    phil = settingsWin(test)
    test.mainloop()