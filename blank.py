import board
import neopixel
import time
# sudo pip3 install rpi_ws281x
# sudo pip3 install adafruit-circuitpython-neopixel

num_pixels = 16*16

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    board.D18, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER
)


pixels.fill((0, 0, 0, 0))
pixels.show()

