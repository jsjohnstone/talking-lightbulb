# talkingLightbulb 💡
A project to make a lightbulb talk

## Summary
Animating a talking lightbulb - a character in [**All Your Wants And Needs Fulfilled Forever**](https://vimeo.com/162170892), a *meta-theatrical ride featuring action packed mime, original songs, and a pulsing electronic score all performed live*, created by The Playground Collective - for the 2016 UK tour.

While this implementation wasn't used in the end (an Ableton Live setup was instead), it was a great opportunity to play with streaming sound to python and seeing what it could do!

![](https://github.com/jsjohnstone/talkinglightbulb/blob/master/docs/app.gif)



## Installation
This app requires the following dependencies:
- cffi==1.14.2
- numpy==1.19.1
- pycparser==2.20
- pyenttec==1.2
- pyserial==3.4
- sounddevice==0.4.0

To install, run:
```pip install -r requirements.txt```

## Usage
There are two things you need to setup before you can start the app:

### Piping sound to the app
When starting the app, you get to choose your input device. 

If you're using a microphone/external sound, pick your systems input device.

If you want to react to sound being generated on the same machine (e.g. from QLab), you'll need to route the sound through a loopback interface such as [Soundflower](https://github.com/mattingalls/Soundflower).

[Soundflower](https://github.com/mattingalls/Soundflower) provides QLab (or your playback software) with an 'output' device it can play music to. If you choose this same device in the application, it'll receive the audio.

### Connecting to DMX
You'll need to connect [ENTTEC DMX Pro](https://www.enttec.com/product/controls/dmx-usb-interfaces/dmx-usb-interface/) (or compatible) adapter and have it connected to the appropriate DMX universe your talking lightbulb lives on.

The DMX channel the lightbulb is on is configured at the top of the script - it's '5' by default but can easily be changed.

### Starting the app
You should be good to go! Just run:
```python3 main.py```

...choose your input and DMX devices and your bulb will be ready to speak.
