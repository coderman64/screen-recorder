"""
    A component of ScreenRecorder that allows one to use ffmpeg.exe to capture
    video from a DirectShow device.
    Copyright (C) 2016  coderman64

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
class capturer:
    def __init__(self, devicename):
        self.devicename = devicename
        self.captureprocess = None
    def startCapture(self,location):
        global startupinfo
        #print(self.devicename)
        self.captureprocess = subprocess.Popen(["ffmpeg","-f","dshow","-i","video="+self.devicename+"",location], startupinfo = startupinfo)
    def stopCapture(self):
        self.captureprocess.terminate()
    def setDevice(self,devicename):
        self.devicename = devicename
if __name__ == "__main__":
    print("here be results...")
    print(listCam())
    print(listMic())
    cap = capturer(listCam()[0])
    try: 
        cap.startCapture("none.mpg")
    except KeyboardInterrupt:
        cap.stopCapture()

# [dshow @ 0
