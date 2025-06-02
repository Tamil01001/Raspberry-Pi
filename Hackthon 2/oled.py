import time
import spidev
import lgpio
from PIL import Image, ImageDraw, ImageFont

class SSD1306:
    def __init__(self, rst_pin, dc_pin, spi_bus=0, spi_device=0):
        self.width = 128
        self.height = 64
        self.rst = rst_pin
        self.dc = dc_pin

        # Setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 8000000
        self.spi.mode = 0

        # Setup GPIO pins using lgpio
        self.h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(self.h, self.rst)
        lgpio.gpio_claim_output(self.h, self.dc)

        self._reset()
        self._init_display()

    def _reset(self):
        lgpio.gpio_write(self.h, self.rst, 0)
        time.sleep(0.1)
        lgpio.gpio_write(self.h, self.rst, 1)
        time.sleep(0.1)

    def _write_command(self, cmd):
        lgpio.gpio_write(self.h, self.dc, 0)
        self.spi.writebytes([cmd])

    def _write_data(self, data):
        lgpio.gpio_write(self.h, self.dc, 1)
        self.spi.writebytes(data)

    def _init_display(self):
        init_commands = [
            0xAE, 0x20, 0x00, 0xB0, 0xC8, 0x00, 0x10, 0x40, 0x81,
            0xFF, 0xA1, 0xA6, 0xA8, 0x3F, 0xA4, 0xD3, 0x00, 0xD5,
            0xF0, 0xD9, 0x22, 0xDA, 0x12, 0xDB, 0x20, 0x8D, 0x14,
            0xAF
        ]
        for cmd in init_commands:
            self._write_command(cmd)

    def image(self, image):
        image = image.convert('1').resize((self.width, self.height))  # Convert to 1-bit and resize
        pixels = list(image.getdata())
        buffer = [0x00] * (self.width * self.height // 8)

        for y in range(self.height):
            for x in range(self.width):
                if pixels[x + y * self.width]:
                    buffer[x + (y // 8) * self.width] |= (1 << (y % 8))

        self.buffer = buffer

    def show(self):
        for page in range(8):
            self._write_command(0xB0 + page)  # Set page address
            self._write_command(0x00)         # Set low column address
            self._write_command(0x10)         # Set high column address
            start = self.width * page
            end = start + self.width
            self._write_data(self.buffer[start:end])

    def cleanup(self):
        self.spi.close()
        lgpio.gpiochip_close(self.h)
