#from dis import show_code
import board
import neopixel
import time
import random
import colorsys
import math
from PIL import Image #sudo python -m pip install --upgrade Pillow  ;; sudo apt-get install libopenjp2-7
 
num_pixels = 16*16
pix_per_row=16
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    board.D18, num_pixels, brightness=0.15, auto_write=False, pixel_order=ORDER
)

basewidth = 16
#img = Image.open('liam.png')
#img = Image.open('ey.png')
img = Image.open('christmas-icons/santa_01.png')
#img = img.resize((basewidth,hsize), Image.ANTIALIAS)
#img.save('somepic.jpg')
rgb_im = img.convert('RGB')

def setpixelRGB(x,y,c):
    if y%2==0:
        pixels[(y+1)*pix_per_row-x-1]=c
    else:
        pixels[(y)*pix_per_row+x]=c

def setpixelHSV(x,y,h,s,v): # between 0 and 1
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    if y%2==0:
        pixels[(y+1)*pix_per_row-x-1]=((int(r*255),int(g*255),int(b*255)))
    else:
        pixels[(y)*pix_per_row+x]=((int(r*255),int(g*255),int(b*255)))

pixels.fill((0,0,0))
pixels.show()
time.sleep(0.1)
while True:
    for y in range(16):
        for x in range(16):
            #setpixelRGB(x,y,(random.randrange(255),random.randrange(255),random.randrange(255)))


            r, g, b = rgb_im.getpixel((x, y))
            setpixelRGB(x,y,(r,g,b))
            #setpixelHSV(x,y,random.random(),1,1)
            
            #time.sleep(0.1)
    pixels.show()