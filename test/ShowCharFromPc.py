from machine import Pin, SPI
from sys import stdin

from Max7219SevenSegment import Max7219SevenSegment

spi = SPI(0, baudrate=100000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(19))
cs = Pin(17, Pin.OUT)

display = Max7219SevenSegment(spi, cs)
display.turn_on()

while True:
    char = stdin.read(1)
    if char >= '!':
        print(f"char '{char}' {ord(char)}")
        display.set_char(0, char)
