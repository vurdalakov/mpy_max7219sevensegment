# A MicroPython library for Raspberry Pi Pico that works with MAX7219 7-segment numeric LED display modules
# MIT License
# Copyright (c) 2023 Vurdalakov
# https://github.com/vurdalakov/mpy_max7219sevensegment

class Max7219SevenSegment:
    
    VERSION = "1.0"

    # constructor

    def __init__(self, spi, cs, number_of_difits = 8):

        self.__number_of_difits = number_of_difits
        self.__buffer = bytearray(self.__number_of_difits)

        self.__digit_masks = [
            0x7E, 0x30, 0x6D, 0x79, 0x33,
            0x5B, 0x5F, 0x70, 0x7F, 0x7B,
            0x77, 0x1F, 0x4E, 0x3D, 0x4F,
            0x47,
            ]
        
        self.__char_masks = [
            0x77, 0x1F, 0x4E, 0x3D, 0x4F,
            0x47, 0x7B, 0x37, 0x06, 0x3C,
            0x57, 0x0E, 0x54, 0x15, 0x1D,
            0x67, 0x73, 0x05, 0x5B, 0x0F,
            0x1C, 0x3E, 0x2A, 0x37, 0x3B, 0x6D,
            ]

        self.__spi = spi
        self._cs = cs
        
        self.__brightness = 7
        self.__reverse = True
    
    # public methods
    
    def turn_on(self):
        self.test_off()
        self.__write_register(self.__REG_DECODE_MODE, 0)
        self.set_brightness(self.__brightness)
        self.__write_register(self.__REG_SCAN_LIMIT, 7)
        self.clear_all()
        self.__write_register(self.__REG_SHUTDOWN, 1)
    
    def turn_off(self):
        self.__write_register(self.__REG_SHUTDOWN, 0)
        
    def test_on(self):
        self.__write_register(self.__REG_DISPLAY_TEST, 1)
        
    def test_off(self):
        self.__write_register(self.__REG_DISPLAY_TEST, 0)

    def set_brightness(self, brightness):
        if (brightness >= 0) and (brightness < 16):
            self.__brightness = brightness
            self.__write_register(self.__REG_INTENSITY, self.__brightness)
            
    def set_reverse(self, reverse):
        self.__reverse = reverse

    def clear(self, index):
            self.set_mask(index, 0x00)
        
    def clear_all(self):
        for index in range(0, self.__number_of_difits):
            self.clear(index)

    def set_digit(self, index, digit, dot = False):
        mask = self.__digit_to_mask(digit, dot)
        self.set_mask(index, mask)

    def set_char(self, index, char, dot = False):
        self.set_mask(index, self.__char_to_mask(char, dot))

    def set_string(self, string, start = 0):
        for i in range(0, len(string)):
            self.set_char(start + i, string[i])

    def set_dot(self, index):
        if self.__is_index_ok(index):
            mask = self.__buffer[index] | 0x80
            self.set_mask(index, mask)

    def clear_dot(self, index):
        if self.__is_index_ok(index):
            mask = self.__buffer[index] & 0x7F
            self.set_mask(index, mask)

    def set_mask(self, index, mask):
        if self.__is_index_ok(index):
            self.__buffer[index] = mask
            if self.__reverse:
                index = 7 - index
            self.__write_register(self.__REG_DIGIT_BASE + index, mask)

    # private methods

    def __is_index_ok(self, index):
        return (index >= 0) and (index < self.__number_of_difits)

    def __digit_to_mask(self, digit, dot):
        if (digit >= 0) and (digit < len(self.__digit_masks)):
            return self.__add_dot(self.__digit_masks[digit], dot)
        else:
            return 0x00

    def __char_to_mask(self, char, dot):
        mask = 0
        if (char >= '0') and (char <= '9'):
            return self.__digit_to_mask(ord(char) - 48, dot)
        elif (char >= 'A') and (char <= 'Z'):
            mask = self.__char_masks[ord(char) - 65]
        elif (char >= 'a') and (char <= 'z'):
            mask = self.__char_masks[ord(char) - 97]
        elif char == '-':
            mask = 0x01
        elif char == '_':
            mask = 0x08
        elif char == '°':
            mask = 0x63
        elif (char == '[') or char == '(':
            mask = 0x4E
        elif (char == ']') or char == ')':
            mask = 0x78
        else:
            mask = 0x00

        return self.__add_dot(mask, dot)

    def __add_dot(self, digit, dot):
        return (digit | 0x80) if dot else digit

    def __write_register(self, register, value):
        self._cs.low()
        self.__spi.write(bytearray([register, value]))
        self._cs.high()

    # private constants

    __REG_NOOP = 0x00
    __REG_DIGIT_BASE = 0x01
    __REG_DECODE_MODE = 0x09
    __REG_INTENSITY = 0x0A
    __REG_SCAN_LIMIT = 0x0B
    __REG_SHUTDOWN = 0x0C
    __REG_DISPLAY_TEST = 0x0F
