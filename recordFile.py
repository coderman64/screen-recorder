"""
    recordFile.py records audio from the default microphone in a background thread using pyaudio
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

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "tmp/tmp.wav"

class recorder:
    def __init__(self):
        self.going = False;
        self.process = None;
        self.filename = "ScreenCapture.mpg"
    def record(self,filename):
        try:
            if self.process.is_alive():
                self.going = False;
        except AttributeError:
            print("test")
        self.process = threading.Thread(target=self._record);
        self.process.start()
        self.filename = filename;
    def _record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        self.going = True;
        
        while self.going:
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        

    def stop_recording(self):
        self.going = False;
        
