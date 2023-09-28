import pygatt
from typing import List

from matrix_message import Message, Color, Lamp, SetDate, Clock, Scoreboard, Image, Timer


class ScreenConnection:
    def __init__(self, address: str):
        self.address = address
        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.device = None
        self.init_connection()

    def init_connection(self):
        while True:
            try:
                self.device = self.adapter.connect(self.address)
                self.device.exchange_mtu(512)
                break
            except pygatt.exceptions.NotConnectedError:
                print("Could not initialize connection, retrying")

    def send(self, message: Message):
        self._send(message.build_message())

    def send_hexstr(self, hexstr: str):
        self._send([int(part, 16) for part in hexstr.split(":")])
    
    def _send(self, data: List[int]):
        data = bytearray(data)
        while True:
            try:
                self.device.char_write_handle(0x0006, data, wait_for_response=True)
                break
            except pygatt.exceptions.NotConnectedError:
                self.init_connection()

    def __del__(self):
        self.adapter.stop()


class Screen:
    def __init__(self, connection: ScreenConnection|str):
        if not isinstance(connection, ScreenConnection):
            connection = ScreenConnection(connection)

        self.connnection = connection
        self.init_clock()

    def init_clock(self):
        self.connnection.send(SetDate.from_timestamp())

    def lamp(self, color: Color):
        self.connnection.send(Lamp(color))

    def clock(self, color: Color, clock_index: int):
        self.connnection.send(Clock(color=color, clock_index=clock_index))
    
    def scoreboard(self, top: int, bottom: int):
        self.connnection.send(Scoreboard(top, bottom))

    def timer(self, action: str):
        self.connnection.send(Timer(action))

    def image(self, pixels: List[List[Color]]):
        self.connnection.send_hexstr("09:00:05:01:03:00:00:00:01")
        self.connnection.send(Image(pixels))
