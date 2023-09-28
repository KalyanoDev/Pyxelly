from typing import List
from dataclasses import dataclass
import time
from datetime import datetime


def split_int_to_list(value: int, bytes: int=1) -> List[int]:
    res = []
    for _ in range(bytes):
        res.append(value & 0xff)
        value >>= 8

    return res


class Message:
    header = [0xff, 0xff]

    def get_content(self) -> List[int]:
        return []

    def build_message(self) -> List[int]:
        content = self.get_content()
        message_size = len(content) + 2 + len(self.header)
        size = split_int_to_list(message_size, bytes=2)

        message = size + self.header + content
        return message


Color = List[int]


@dataclass
class Lamp(Message):
    header = [0x02, 0x02]
    color: Color

    def get_content(self) -> List[int]:
        return self.color


@dataclass
class SetDate(Message):
    header = [0x01, 0x80]
    
    year: int
    month: int
    day: int
    dow: int
    h: int
    m: int
    s: int

    @classmethod
    def from_timestamp(cls, timestamp: int|float|None=None):
        if timestamp is None:
            timestamp = time.time()
        
        date = datetime.fromtimestamp(timestamp)
        return cls(date.year, date.month, date.day, date.weekday()+1, date.hour, date.minute, date.second)
        
    def get_content(self) -> List[int]:
        content = []

        content.append(self.year & 0xff)
        content.append(self.month)
        content.append(self.day)
        content.append(self.dow)
        content.append(self.h)
        content.append(self.m)
        content.append(self.s)

        return content
    

@dataclass
class Clock(Message):
    header = [0x06, 0x01]
    
    color: Color

    clock_index: int = 0
    toggle_date: bool = False
    format_24h: bool = True

    def get_content(self) -> List[int]:
        content = []

        config_byte = self.clock_index
        config_byte |= self.toggle_date * 0x80
        config_byte |= self.format_24h * 0x40

        content.append(config_byte)
        content.extend(self.color)
        return content


@dataclass
class Scoreboard(Message):
    header = [0x0a, 0x80]
    top: int = 0
    bottom: int = 0

    def get_content(self) -> List[int]:
        content = []
        content.extend(split_int_to_list(self.top, bytes=2))
        content.extend(split_int_to_list(self.bottom, bytes=2))
        return content

   
@dataclass
class ScreenType(Message):
    header = [0x04, 0x01]
    
    screen: int
    def get_content(self) -> List[int]:
        return [self.screen]


@dataclass
class Image(Message):
    header = [0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00]

    pixels: List[List[Color]]

    def get_content(self) -> List[int]:
        content = []

        for line in self.pixels:
            for pixel in line:
                content.extend(pixel)

        return content
    

@dataclass
class Timer(Message):
    header = [0x09, 0x80]
    actions = ["reset", "start", "pause", "resume"]

    action: str

    def get_content(self) -> List[int]:
        return [self.actions.index(self.action)]
