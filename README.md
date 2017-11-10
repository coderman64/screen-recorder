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

## what is going on?

Here's what I have on the to-do list for this project:

* add webcam support, so you can (optionally) see yourself in the lower corner of the screen.
* change the audio imput from pyaudio to ffmpeg and DirectShow, which is perfectly fine for recording audio. Plus, less dependencies = more better! (Grammar? Don't know what you are talking about.)
* add more customization options, perhaps in a separate window.
* keep it light, simple, and working! (hopefully)

Webpage:
* change the website in Edge & IE so it is a still image instead of a gif. As it is right now, Edge & IE use _way_ too much RAM to render it.
