from spidev import SpiDev
import RPi.GPIO
import time

class ST7789VW(object):

    # Back light
    GPIO_BL = 24
    # Data/Command select
    GPIO_DC = 25
    # Reset
    GPIO_RST = 27

    @property
    def size(self):
        return (self._width, self._height)

    def __init__(self, spi, gpio):
        self._spi = spi
        self._gpio = gpio
        self._width = 240
        self._height = 240

    def init_display(self):
        self.hard_reset()
        # wip

    def hard_reset(self):
        # RESX Pulse Longer than 9us
        gpio = self._gpio
        rst = self.GPIO_RST
        gpio.output(rst, gpio.HIGH)
        time.sleep(0.00001)
        gpio.output(rst, gpio.LOW)
        time.sleep(0.00001)
        gpio.output(rst, gpio.HIGH)
        time.sleep(0.00001)

    def _command(self, cmd):
        gpio = self._gpio
        gpio.output(self.GPIO_DC, gpio.LOW)
        self._spi.writebytes([cmd])

    def _data(self, values):
        gpio = self._gpio
        gpio.output(self.GPIO_DC, gpio.HIGH)
        self._spi.writebytes2(values)

    def _write(self, value):
        cmd, values = value
        self._command(cmd)
        if value is not None:
            self._data(values)

    @classmethod
    def load(cls, spi_bus, spi_device, spi_max_speed_hz=40000000):
        spi = SpiDev(spi_bus, spi_device)
        spi.max_speed_hz = spi_max_speed_hz
        return cls(spi, RPi.GPIO)
