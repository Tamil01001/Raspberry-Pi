# pioneer_buzzer.py

import smbus
import time

class PioneerBuzzer:
    def __init__(self, i2c_addr=0x20, bus_num=1, pin=7):
        self.i2c_addr = i2c_addr
        self.bus = smbus.SMBus(bus_num)
        self.pin = pin  # P7 is usually connected to the buzzer
        self.OUTPUT_PORT1 = 0x03
        self.CONFIG_PORT1 = 0x07
        self._setup()

    def _setup(self):
        # Set all Port1 pins as output (0 = output)
        self.bus.write_byte_data(self.i2c_addr, self.CONFIG_PORT1, 0x00)
        # Start with all outputs HIGH (buzzer OFF)
        self.bus.write_byte_data(self.i2c_addr, self.OUTPUT_PORT1, 0xFF)

    def on(self):
        """Turn the buzzer ON (active low on P7)."""
        state = self.bus.read_byte_data(self.i2c_addr, self.OUTPUT_PORT1)
        state &= ~(1 << self.pin)  # Set P7 to 0
        self.bus.write_byte_data(self.i2c_addr, self.OUTPUT_PORT1, state)

    def off(self):
        """Turn the buzzer OFF (inactive high on P7)."""
        state = self.bus.read_byte_data(self.i2c_addr, self.OUTPUT_PORT1)
        state |= (1 << self.pin)  # Set P7 to 1
        self.bus.write_byte_data(self.i2c_addr, self.OUTPUT_PORT1, state)

    def beep(self, duration=1.0):
        """Beep the buzzer for a set duration in seconds."""
        self.on()
        time.sleep(duration)
        self.off()

