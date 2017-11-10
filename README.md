# screen-recorder
A python GUI for recording your screen

This program provides an easy GUI-based interface to ffmpeg's gdigrab feature, which allows you to take a video recording of your screen in Windows. I also used pyaudio to record audio as your screen is being recorded.

## how to get it running
This should work with python version 3.5 or later, as long as you have tkinter and pyaudio installed. Tkinter usually comes with the default python installation, and you can install pyaudio through one of the following commands:
```
pip install pyaudio
```
or
```
python -m pip install pyaudio
```
additionally, you need to get ffmpeg.exe from the windows package [here](https://ffmpeg.zeranoe.com/builds/). then just take ffmpeg.exe from the bin folder, and put it in the same folder as the script
