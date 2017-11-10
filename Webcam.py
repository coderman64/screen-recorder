"""
    A component of ScreenRecorder that allows one to use ffmpeg.exe to capture
    video from a DirectShow device.
"""

import subprocess
from threading import Thread

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

def listCam():
    global startupinfo
    process1 = subprocess.run(["ffmpeg.exe","-list_devices","true","-f","dshow","-i","dummy"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT, startupinfo=startupinfo)
    result = str(process1.stdout).replace("\\r\\n","\n").replace("\\\\","\\")
    result = result[result.find("[dshow @"):result.find("DirectShow audio")].splitlines()
    result2 = []
    for i in result:
        if i[i.find("]")+1:].strip(" ").startswith("\""):
            result2.append(i[i.find("]")+1:].strip(" \""))
    return result2

def listMic():
    global startupinfo
    process1 = subprocess.run(["ffmpeg.exe","-list_devices","true","-f","dshow","-i","dummy"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT, startupinfo=startupinfo)
    result = str(process1.stdout).replace("\\r\\n","\n").replace("\\\\","\\")
    result = result[result.find("DirectShow audio"):].splitlines()
    result2 = []
    for i in result:
        if i[i.find("]")+1:].strip(" ").startswith("\""):
            result2.append(i[i.find("]")+1:].strip(" \""))
    return result2
class webcamCapturer:
    def __init__(self, devicename):
        self.devicename = devicename
        self.captureprocess = None
    def startCaputure(self,location):
        global startupinfo
        self.catureprocess = Popen(["ffmpeg","-f","dshow","-i","video=\""+self.devicename+"\"",location], startupinfo=startupinfo)
    def stopCapture(self):
        self.captureprocess.terminate()
if __name__ == "__main__":
    print("here be results...")
    print(listCam())
    print(listMic())

# [dshow @ 0
