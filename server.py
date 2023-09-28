from typing import List
from fastapi import FastAPI
from matrix_message import Color

from matrix_handler import Screen

# Edit with the address of your device
TARGET_ADDR = "aa:bb:cc:dd:ee:ff"

SCREEN = Screen(TARGET_ADDR)

app = FastAPI()


@app.get("/clock/")
def display_clock(r: int=0, g: int=0, b: int=0, clock_index: int=0):
    SCREEN.clock([r, g, b], clock_index)
    return {}


@app.get("/scoreboard/")
def set_scoreboard(top: int=0, bottom: int=0):
    SCREEN.scoreboard(top, bottom)
    return {}

@app.get("/lamp/")
def set_lamp(r: int=0, g: int=0, b: int=0):
    SCREEN.lamp([r, g, b])
    return {}

@app.post("/image/")
def display_image(pixels: List[List[Color]]):
    SCREEN.image(pixels)
    return {}

@app.get("/raw_message/")
def raw_message(hexstr: str):
    SCREEN.connnection.send_hexstr(hexstr)
    return {}

@app.get("/timer/start")
def timer_start():
    SCREEN.timer("start")
    return {}

@app.get("/timer/pause")
def timer_pause():
    SCREEN.timer("pause")
    return {}

@app.get("/timer/reset")
def timer_reset():
    SCREEN.timer("reset")
    return {}

@app.get("/timer/resume")
def timer_resume():
    SCREEN.timer("resume")
    return {}


