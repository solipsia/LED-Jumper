import board
import neopixel
import time
# sudo pip3 install rpi_ws281x
# sudo pip3 install adafruit-circuitpython-neopixel

num_pixels = 16*16

pixels = neopixel.NeoPixel(
    board.D18, num_pixels, brightness=0.1, auto_write=False, pixel_order=neopixel.GRB
)


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def rainbow_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()

while True:

    rainbow_cycle() 


