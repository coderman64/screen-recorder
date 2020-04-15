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
import os

class cmdGen:
    def __init__(self):
        self.fps = 30
        self.source = "desktop"
        self.encoder = 'mpeg4'
        self.hwaccel = None
        self.drawMouse = 1
        self.enableWebcam = False
        self.audList = [None]
    def config(self,
                fps=None,source=None,encoder=None,
                hwaccel='unchanged',drawMouse=None,
                webcam=None,audList=None):
        if fps: self.fps = fps
        if source: self.source = source
        if encoder: self.encoder = encoder
        if hwaccel != 'unchanged': self.hwaccel = hwaccel
        if drawMouse: self.drawMouse = 0 if not self.drawMouse else 1
        if webcam: self.enableWebcam = bool(webcam)
        if audList: self.audList = audList
    def setSource(self,isWindow,windowName=""):
        if not isWindow:
            self.source = "desktop"
        else:
            self.source = "title="+windowName
    def setFps(self,fps):
        self.fps = fps
    def setEncode(self,encoder):
        self.encoder = encoder
    def getCmd(self,filename):
        finalCmd = ["ffmpeg.exe","-f","gdigrab"]
        finalCmd.extend(['-i',self.source])
        finalCmd.extend(['-framerate',str(self.fps)])
        finalCmd.extend(['-c:v',self.encoder])
        if self.encoder == 'mpeg4':
            finalCmd.extend(['-q:v','7'])
        if self.hwaccel: 
            finalCmd.extend(['-hwaccel',self.hwaccel])
        finalCmd.extend(['-draw_mouse',str(self.drawMouse)])
        finalCmd.extend(["-y", filename])
        print(finalCmd)
        return finalCmd
    def getCvtCmd(self,filename):
            # if self.rcchecked.get():
            #     self.mergeProcess = subprocess.Popen(args= ["ffmpeg","-i",'tmp/tmp.mkv','-i','tmp/tmp.wav','-i','tmp/webcamtmp.mkv','-filter_complex','[2:v] scale=640:-1 [inner]; [0:0][inner] overlay=0:0 [out]',"-shortest",'-map','[out]','-y',"ScreenCaptures/"+self.filename])
            # else:
            #     self.mergeProcess = subprocess.Popen(args= ["ffmpeg","-i",'tmp/tmp.mkv','-i','tmp/tmp.wav',"-shortest",'-y',"ScreenCaptures/"+self.filename], startupinfo=startupinfo)
        print("ACK")
        finalCmd = ["ffmpeg.exe"]
        finalCmd.extend(['-i','tmp/tmp.mkv'])
        for i in range(len(self.audList)):
            finalCmd.extend(['-i','tmp/tmp_'+str(i)+'.wav'])
        if len(self.audList) > 0:
            finalCmd.extend(['-af','amerge=inputs='+str(len(self.audList))+'[aud1]; [aud1] apad [out]','-ac',str(len(self.audList))])
        # finalCmd.extend(['-c:v',self.encoder])
        if self.enableWebcam:
            finalCmd.extend(['-i','tmp/webcamtmp.mkv','-vf','[2:v] scale=640:-1 [inner]; [0:0][inner] overlay=0:0 [out]','-map','[out]'])
        if self.hwaccel: 
            finalCmd.extend(['-hwaccel',self.hwaccel])
        if self.encoder == 'h264_nvenc':        
            finalCmd.extend(['-c:v',self.encoder])
        finalCmd.extend(['-shortest'])
        finalCmd.extend(["-y", filename])
        print(finalCmd)
        return finalCmd

if __name__ == "__main__":
    cg = cmdGen()
    cg.setEncode("h264_nvenc")
    cg.setFps(60)
    cg.setSource(False)
    print(cg.getCmd("tmp"))