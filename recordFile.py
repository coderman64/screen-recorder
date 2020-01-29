"""
    recordFile.py records audio from the default microphone in a background 
    thread using pyaudio.
    Copyright (C) 2016 coderman64

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
import pyaudio
import wave
import threading
import time
import subprocess
from tkinter import messagebox

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "tmp/tmp.wav"

class recorder:
    def __init__(self):
        self.going = False      # is the process running?
        self.process = None     # stores a reference to the background thread
        self.filename = ""      # the name of the file to record to 
        self.p = pyaudio.PyAudio()
        self.devices = [None]
        self.error = False
    def record(self,filename):
        # end the process before starting a new one
        if self.process and self.process.is_alive():
            self.going = False
        self.error = False
        
        # start a recording thread
        self.process = threading.Thread(target=self._record)
        self.process.start()
        self.filename = filename
    def _record(self):
        try:
            # initialize pyaudio
            streams = []
            frames = [] # stores audio data
            for i in range(len(self.devices)):
                streams.append(self.p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK,
                            input_device_index=self.devices[i]))
                frames.append([])

            print("* recording")

            self.going = True   # let the system know that we are running
            
            while self.going:   # stream the audio into "frames"
                for i in range(len(self.devices)):
                    data = streams[i].read(CHUNK)
                    frames[i].append(data)

            print("* done recording")

            # stop recording
            for i in range(len(self.devices)):
                streams[i].stop_stream()
                streams[i].close()

            # write the audio data to a file (tmp/tmp.wav)
            for i in range(len(self.devices)):
                wf = wave.open(self.filename[:self.filename.find(".")]+"_"+str(i)+self.filename[self.filename.find("."):], 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames[i]))
                wf.close()
        except Exception as e:
            self.error = True
            messagebox.showerror("AUDIO ERROR","ERROR ENCOUNTERED RECORDING AUDIO: "+str(e))
    def getDeviceCount(self):
        return self.p.get_device_count()
    def getDeviceName(self,deviceID):
        return self.p.get_device_info_by_index(deviceID)["name"]
    def isInputDevice(self,deviceID):
        return int(self.p.get_device_info_by_index(deviceID)["maxInputChannels"]) > 0
    def getAPIName(self,deviceID):
        return self.p.get_host_api_info_by_index(self.p.get_device_info_by_index(deviceID)["hostApi"])["name"]
    def setToDefault(self):
        self.devices = [None]
    def setToDevices(self,devices):
        self.devices = devices
    def stop_recording(self):
        self.going = False
    def destroy(self):
        self.p.terminate()
        
