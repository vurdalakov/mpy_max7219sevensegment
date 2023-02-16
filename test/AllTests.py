from machine import Pin, SPI
from time import sleep

from Max7219SevenSegment import Max7219SevenSegment

spi = SPI(0, baudrate=100000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(19))
cs = Pin(17, Pin.OUT)

display = Max7219SevenSegment(spi, cs)
display.turn_on()

display.test_on()
sleep(1)
display.test_off()
sleep(1)

display.set_string('HELLO   ')
sleep(1)

display.set_string('PI PICO ')
sleep(1)

display.set_string('12345678')
sleep(1)

display.clear_all()
sleep(1)

for i in range(0, 16):
    display.set_digit(i % 8, i)
    sleep(0.5)

sleep(1)

for i in range(7, -1, -1):
    display.clear(i)
    sleep(0.5)

display.set_string('__-°°-__')
sleep(1)

display.clear_all()
sleep(1)

for i in range(0, 8):
    display.clear_dot(i - 1)
    display.set_dot(i)
    sleep(0.25)

for i in range(7, -1, -1):
    display.clear_dot(i)
    display.set_dot(i - 1)
    sleep(0.25)

sleep(1)

display.set_brightness(0)
display.set_string('0')
sleep(0.5)

for i in range(1, 16):
    display.set_brightness(i)
    display.set_string(str(i))
    sleep(0.5)

display.clear_all()
display.set_brightness(7)
sleep(1)

for i in range(0, 16):
    display.set_digit(0, i)
    sleep(0.5)

display.clear_all()
sleep(1)

def char_range(c1, c2):
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)

for c in char_range('a', 'z'):
    display.set_char(0, c)
    sleep(0.5)

display.clear_all()
sleep(1)

for c in char_range('A', 'Z'):
    display.set_char(0, c)
    sleep(0.5)

display.clear_all()
sleep(1)

display.set_char(0, '-')
sleep(0.5)
display.set_char(0, '_')
sleep(0.5)
display.set_char(0, '°')
sleep(0.5)
display.set_char(0, ' ')

sleep(1)

display.set_string('Error', 2)
