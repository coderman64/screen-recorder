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

class cmdGen:
    def __init__(self):
        self.fps = 60
        self.source = "desktop"
        self.encoder = 'mpeg4'
        self.hwaccel = None
        self.drawMouse = 1
    def config(self,fps=None,source=None,encoder=None,hwaccel='unchanged',drawMouse=None):
        if fps: self.fps = fps
        if source: self.source = source
        if encoder: self.encoder = encoder
        if hwaccel != 'unchanged': self.hwaccel = hwaccel
        if drawMouse: self.drawMouse = 0 if not self.drawMouse else 1
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
        print("ACK")
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
        return finalCmd

if __name__ == "__main__":
    cg = cmdGen()
    cg.setEncode("h264_nvenc")
    cg.setFps(60)
    cg.setSource(False)
    print(cg.getCmd("tmp"))