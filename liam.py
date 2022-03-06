from dis import show_code
import board
import neopixel
import time
import random
import colorsys
import math

num_pixels = 16*16
ORDER = neopixel.RGB #GRB

pixels = neopixel.NeoPixel(
    board.D18, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)




pixels.fill((255,255,0))
pixels.show()
