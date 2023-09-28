This repository presents a Python API server to drive cheap 32x32 pixel bluetooth photo frames, a cheap alternative to the divoom screens.

This display can usualy only be controlled with a proprietary app. This project allows to control it using a basic HTTP API, for instance to display custom images. The code of this project can also be used as a python module.

Here are some references to the display: 
- Its dimensions are 20cm by 20 cm
- It does exist in 16x16 and 32x32 pixels. Only the 32x32 pixels version has been tested yet.
- Powered by an usb-c socket, controllable via bluetooth
- The display does not have a specific brand, the box only says "Pixel Display"
- The best name for the display would be "iDotMatrix", which is the name of the app used to control it
- It can be bought on aliexpress [here](https://s.click.aliexpress.com/e/_DCVT4kf), [here](https://s.click.aliexpress.com/e/_DnccY5Z), [here](https://s.click.aliexpress.com/e/_DCFg67N) or [here](https://s.click.aliexpress.com/e/_DBHNuzh) (these are affiliate links)

Disclaimer: this project is not official



This repo is currently a WIP, only a small subset of the protocol has been implemented.
The code is quite crude, but it can already be used as is to send custom images to the screen. A detailed explanation of the protocol and a cleaner API will come later.

## Functionalities
 
Here is a list of the display functionalities currently handled:
- Display of any 32*32 RGB image
- Live clock with custom color and selection of preset backgrounds
- Lamp mode (all pixels lit with the same custom color)
- Timer: start, pause, resume, reset
- Scoreboard

## Installation

- `sudo apt install uvicorn`
- `pip install -r requirements.txt`

## Basic usage

Find the bluetooth address of your device using the bluetooth device manager of your os.

Edit `server.py` to set `TARGET_ADDR` to the address of your device, then run the server using `uvicorn server:app`.

Unless it is run as root, it will prompt for your password in order to have the rights to access bluetooth.

Then the documentation of the API can be found at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

`image_sender.py` is an example of how to send an image to the screen.


