#import board
#import neopixel
import time
import random
import colorsys
import copy
from turtle import clear
# sudo pip3 install rpi_ws281x
# sudo pip3 install adafruit-circuitpython-neopixel 
import numpy as np
import matplotlib.pyplot as plt
import math

from PIL import Image,ImageDraw,ImageFont #sudo python -m pip install --upgrade Pillow  ;; sudo apt-get install libopenjp2-7


orientation=0 #0=plug top
mode=5
modes=6
numx=16
numy=16
num_pixels = 16*16
mode_pic=5
wallblock = -2 #block type
clearblock = -1 #block type
coinblock = -3 # block type

#pixels = neopixel.NeoPixel(
#    board.D18, num_pixels, brightness=0.1, auto_write=False, pixel_order=neopixel.GRB
#)
pixels=[(0,0,0) for x in range(numx*numy)] 

print('\033[?25l', end="") # hide cursor
def pixelsfill(col):
    for x in range(numx):
        for y in range(numy):
            setpixelRGB(x,y,col)


def pixelsshow():
    for y in range(numy):
        for x in range(numx):
            if y%2==0:
                r=pixels[(y+1)*numx-x-1][0]
                g=pixels[(y+1)*numx-x-1][1]
                b=pixels[(y+1)*numx-x-1][2]
            else:
                r=pixels[(y)*numx+x][0]
                g=pixels[(y)*numx+x][1]
                b=pixels[(y)*numx+x][2]
            if r==0 and g==0 and b==0:
            #print(f'\x1b[38;2;{r};{g};{b}m# \x1b[0m',end='') # print # char in RGB
                print(f'\x1b[31m  \x1b[0m',end='') # print # char in RGB
            else:
                print(f'\x1b[38;2;{r};{g};{b}m# \x1b[0m',end='') # print # char in RGB
        print('') # new line
    for y in range(numy):
        print(f'\033[A',end='') # move cursor to top

def setpixelRGB(x,y,c):
    if y%2==0:
        pixels[max(min(y+1,numy-1),0)*numx-max(min(x,numx-1),0)-1]=c
    else:
        pixels[(y)*numx+max(min(x,numy-1),0)]=c

def setpixelHSV(x,y,h,s,v): # between 0 and 1
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    if y%2==0:
        pixels[(y+1)*numx-x-1]=((int(r*255),int(g*255),int(b*255)))
    else:
        pixels[(y)*numx+x]=((int(r*255),int(g*255),int(b*255)))

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
            if mode!=1: 
                break
        if mode!=1: 
            break
        pixelsshow()

def solvemaze(maze,start,coins):
    stepcounter=0
    eatencoin=-1
    steps=[]#holds the list of coordinates for each step number
    succeed=False #when this becomes true, solution found. 
    fail=False#when this becomes true, no solution is issible. 
    #avoid start and end being inside a wall
    maze[start[0]][start[1]]=clearblock
    for coin in coins:
        maze[coin[0]][coin[1]]=clearblock
    steps.append([start]) #start at the start
    maze[start[0]][start[1]]=0

    #step 0 is start, for every available spot around it, call those step 1, the repeat until one of the available
    #spots is the end, then you know there is at least one path.
    #walk back from the end on each step that's 1 less back to 0 - that's the shortest path

    while not succeed and not fail:
        listofcoordinates=[] # holds all coordinates of current step number
        for step in steps[stepcounter]: #for each of those coordinates
            if step[0] in range(numy) and step[1]-1 in range(numx):
                if maze[step[0]][step[1]-1]==clearblock: #path is left of that block, so add to list of the next step number an update the maze array
                    listofcoordinates.append((step[0],step[1]-1))
                    maze[step[0]][step[1]-1]=stepcounter+1
            if  step[0] in range(numy) and step[1]+1 in range(numx):
                if maze[step[0]][step[1]+1]==clearblock: #path right
                    listofcoordinates.append((step[0],step[1]+1))
                    maze[step[0]][step[1]+1]=stepcounter+1
            if step[0]-1 in range(numy) and step[1] in range(numx):
                if maze[step[0]-1][step[1]]==clearblock: #path up
                    listofcoordinates.append((step[0]-1,step[1]))
                    maze[step[0]-1][step[1]]=stepcounter+1
            if step[0]+1 in range(numy) and step[1] in range(numx):
                if maze[step[0]+1][step[1]]==clearblock: #path left
                    listofcoordinates.append((step[0]+1,step[1]))
                    maze[step[0]+1][step[1]]=stepcounter+1
        steps.append(listofcoordinates)    
        #if end in listofcoordinates:
        for num,coin in enumerate(coins):
            if coin in listofcoordinates:
                succeed=True
                end=(coin[0],coin[1])
                eatencoin=num
        if listofcoordinates == []:
            fail=True    
        stepcounter+=1

    #capture solution into new list by walking back from the end to start
    solution=[] #coords of each sequential step between start and end
    if succeed:
        pos=[0 for i in range(2)] #pos holds the current position of the walker
        pos[0]=end[0] # start at the end 
        pos[1]=end[1]
        solution.append(pos[:])
        for i in range(stepcounter):
            # check which direction has the lowest step count, i.e. is shortest path to start. 
            # load the step number into each direction.
            if pos[0]-1 in range(numy) and pos[1] in range(numx):
                up=maze[pos[0]-1][pos[1]]
            else:
                up=wallblock
            if pos[0]+1 in range(numy) and pos[1] in range(numx):
                down=maze[pos[0]+1][pos[1]]
            else:
                down=wallblock
            if pos[0] in range(numy) and pos[1]-1 in range(numx):
                left=maze[pos[0]][pos[1]-1]
            else:
                left=wallblock
            if pos[0] in range(numy) and pos[1]+1 in range(numx):
                right=maze[pos[0]][pos[1]+1]
            else:
                right=wallblock
            direction=0 #0 is up, 1 is right etc
            if (right<=up or up<0) and (right<=down or down<0) and (right<=left or left<0) and right>clearblock:
                direction=1
            if (down<=up or up<0) and (down<=right or right<0) and (down<=left or left<0)and down>clearblock:
                direction=2
            if (left<=up or up<0) and (left<=down or down<0) and (left<=right or right<0) and left>clearblock:
                direction=3
            #move the position in the chosen direction
            if direction==0:#up
                pos[0]=pos[0]-1
                pos[1]=pos[1]
            if direction==1:#right
                pos[0]=pos[0]
                pos[1]=pos[1]+1
            if direction==2:#down
                pos[0]=pos[0]+1
                pos[1]=pos[1]
            if direction==3:#left
                pos[0]=pos[0]
                pos[1]=pos[1]-1
            solution.append(pos[:]) #add the new position to the solution list
        solution= solution[::-1]#reverse the list so its start to end
    return(solution,eatencoin)


def snakemode():
    maze = [[clearblock for x in range(numx)] for y in range(numy)] #generate blank maze with [y][x] based coordinates
    

     
    #start=(3,3)
    #end=(9,15)
    #start=(random.randrange(0,numy),random.randrange(0,numx))
    #end=(random.randrange(0,numy),random.randrange(0,numx))

    #snakehead=(random.randrange(0,numy),random.randrange(0,numx))
    snakebody=[]
    snakebody.append((random.randrange(0,numy),random.randrange(0,numx)))
    snaketargetlength=1
    coins=[]
    coins.append((1,10))
    coins.append((10,5)) 
    solution=[]
    gameover=False

    while not gameover:
        maze = [[clearblock for x in range(numx)] for y in range(numy)] #generate blank maze with [y][x] based coordinates
        #imprint snake onto maze for routing
        for seg in snakebody:
            maze[seg[0]][seg[1]]=wallblock

        solution,eatencoin = solvemaze(maze,snakebody[0],coins)
        if not solution:
            gameover=True
            pixelsfill((255,0,0))
            pixelsshow()
            time.sleep(0.05)
            break

        if len(solution)<=2:#at the coin
            coins.remove(coins[eatencoin])#remove eaten coin
            coins.append((random.randrange(0,numy),random.randrange(0,numx)))#new coin
            #grow snake here
            snaketargetlength+=1

        #copy solution to pixel display:
        for x in range(numx):
            for y in range(numy):
                if solution and [y,x] in solution:
                    p=1
                    #setpixelRGB(x,y,(255,0,0)) # draw path
                else:
                    if maze[y][x] == wallblock:
                        setpixelRGB(x,y,(255,255,255)) #wall block
                    else:
                        setpixelRGB(x,y,(25,25,25)) #clear block
        # show coins
        for coin in coins:
            setpixelRGB(coin[1],coin[0],(255,255,0)) #coin block
        # show snake:
        for seg in snakebody:
            setpixelRGB(seg[1],seg[0],(0,255,0))  
        pixelsshow()
        time.sleep(0.05)

        #move snake
        nextsnake=copy.deepcopy(snakebody)
        for i in range(len(snakebody)-1):
            nextsnake[i+1]=snakebody[i]
        nextsnake[0]=solution[1] # move head to coin position
        if len(nextsnake)<snaketargetlength: # snake needs to grow
            nextsnake.append(snakebody[len(snakebody)-1])
        snakebody=copy.deepcopy(nextsnake)

def pong():
    x=float(random.randrange(numx-2)+1)
    y=float(random.randrange(numy-2)+1)
    xdir=1.0
    ydir=1.0
    pad1=float(numx/2)
    pad2=float(numx/2)
    pad1speed=1
    pad1target=float(numx/2)
    pad2speed=1
    pad2target=float(numx/2)
    pad1color=(255,0,0)
    pad2color=(0,0,255)

    
    while mode==2:
        pixelsfill((0, 0, 0))
        x=x+xdir
        bounce=random.uniform(0.5, 2.0)
        if int(x+xdir)<0 or int(x+xdir)>=numx:
            xdir=-xdir
        y=y+ydir
        if int(y+ydir)<1 or int(y+ydir)>=numy-1:
            ydir=-abs(ydir)/ydir*bounce
        # calc paddle positions: 
        if ydir<0: #coming towards paddle 1
            if (x+xdir*(y-1)/(-ydir)) >= numx:
                pad1target = numx-((x+xdir*(y-1))-numx)
            elif (x+xdir*(y-1))<0:
                pad1target = -(x+xdir*(y-1)/(-ydir))
            else:
                pad1target=x+xdir*(y-1)/(-ydir)
        if ydir>0: #coming towards paddle 2
            if (x+xdir*(numy-y-1)/(ydir)) >= numx:
                pad2target = numx-((x+xdir*(numy-y-1)/ydir)-numx)-1
            elif (x+xdir*(numy-y))<0:
                pad2target = -(x+xdir*(numy-y-1)/ydir)
            else:
                pad2target=x+xdir*(numy-y-1)/ydir
        #now move to target:
        pad1speed = abs(pad1-pad1target)/5
        if pad1target>pad1:
            pad1+=min(pad1speed,pad1target-pad1)
        elif pad1target<pad1:
            pad1-=min(pad1speed,pad1-pad1target)
        pad2speed = abs(pad2-pad2target)/5
        if pad2target>pad2:
            pad2+=min(pad2speed,pad2target-pad2)
        elif pad2target<pad2:
            pad2-=min(pad2speed,pad2-pad2target)
        #limit pad movement to edge of screen
        pad1 = min(max(1,pad1),numx-3)
        pad2 = min(max(1,pad2),numx-3)
        #ball
        setpixelRGB(int(x),int(y),(0,255,0))
        #paddle 1
        setpixelRGB(int(pad1),0,pad1color)
        setpixelRGB(int(pad1)-1,0,pad1color)
        setpixelRGB(int(pad1)+1,0,pad1color)
        #paddle 2
        setpixelRGB(int(pad2),numx-1,pad2color)
        setpixelRGB(int(pad2)-1,numx-1,pad2color)
        setpixelRGB(int(pad2)+1,numx-1,pad2color)
        pixelsshow()
        time.sleep(0.04)

def bounceball():
    balls=3
    gravity=0.025
    boostthreshold=0.3
    booststrength=0.773
    minxv = 0.05
    maxxv = 0.2
    x = [random.random()*(numx-1) for i in range(balls)]
    y = [random.random()*(numy-1) for i in range(balls)]
    vx = [random.uniform(0.05, 0.12) for i in range(balls)]
    vy = [0.0 for i in range(balls)]
    hue= [random.random() for i in range(balls)]
    hue[0]=0
    hue[1]=0.3
    hue[2]=0.7
    bounceloss=[random.uniform(0.5, 0.8) for i in range(balls)]
    while mode==3:
        pixelsfill((0, 0, 0)) # clear screen
        for ball in range(balls):
            vy[ball]=vy[ball]-gravity
            y[ball]+=vy[ball]
            x[ball]+=vx[ball]
            if y[ball]<0: 
                y[ball]=-y[ball]
                vy[ball]=-vy[ball]*bounceloss[ball]
                if abs(vy[ball])<boostthreshold: # boost
                    vy[ball]=booststrength
                    y[ball]=0
                    vx[ball] = random.uniform(minxv, maxxv)
            if x[ball]<0:
                x[ball]=-x[ball]
                vx[ball]=-vx[ball] 
            if x[ball]>numx-1:
                x[ball]=numx-1-(x[ball]-(numx-1))
                vx[ball]=-vx[ball] 
            setpixelHSV(int(round(x[ball],0)),int(round(y[ball],0)),hue[ball],1,1)#draw ball
        pixelsshow()

def snow():
    balls=numx
    gravity=[random.uniform(0.005, 0.08) for i in range(balls)]
    x = [i for i in range(balls)]
    y = [random.random()*(numy-1) for i in range(balls)]
    y = [(numy-1) for i in range(balls)]
    vx = [0 for i in range(balls)]
    vy = [0.0 for i in range(balls)]
    hue= [random.random() for i in range(balls)]
    while mode==0:
        pixelsfill((0, 0, 0)) # clear screen
        for ball in range(balls):
            vy[ball]=-gravity[ball]
            y[ball]+=vy[ball]
            if y[ball]<0: 
                y[ball]=numy-1
            setpixelHSV(int(round(x[ball],0)),int(round(y[ball],0)),hue[ball],0.1,1)#draw ball
        pixelsshow()

def picmodewithsnow():
    balls=numx
    gravity=[random.uniform(0.005, 0.08) for i in range(balls)]
    x = [i for i in range(balls)]
    y = [(numy-1) for i in range(balls)]
    y = [(0) for i in range(balls)]
    vy = [0.0 for i in range(balls)]
    hue= [random.random() for i in range(balls)]
    imgs=[]
    folder='/home/pi/leds/christmas-icons/'
    folder='christmas-icons/'
    imgs.append(Image.open(folder+'39.png').convert('RGB'))#bauble
    imgs.append(Image.open(folder+'28b.png').convert('RGB'))#candy stick
    imgs.append(Image.open(folder+'37.png').convert('RGB'))#mistletoe
    #imgs.append(Image.open('christmas-icons/56.png').convert('RGB'))#xmas tree1
    imgs.append(Image.open(folder+'59.png').convert('RGB'))#xmas tree2 (better)
    imgs.append(Image.open(folder+'60.png').convert('RGB'))#xmas hat
    #imgs.append(Image.open(folder+'85.png').convert('RGB'))# father xmas
    #imgs.append(Image.open(folder+'87.png').convert('RGB'))# skate
    #imgs.append(Image.open('christmas-icons/89.png').convert('RGB'))# snowman 1
    #imgs.append(Image.open(folder+'90.png').convert('RGB'))# snowman 2 (better)
    imgs.append(Image.open(folder+'93.png').convert('RGB'))# sock 1 (better)
    imgs.append(Image.open(folder+'94.png').convert('RGB'))# sock 2
    imgs.append(Image.open(folder+'95.png').convert('RGB'))# sock 3 (best)
    #imgs.append(img.resize((basewidth,hsize), Image.ANTIALIAS)
    #rgb_im = img.convert('RGB')
    random.shuffle(imgs)
    index=0 # start with first image
    duration=5#seconds per image
    timer=time.perf_counter() # start timer

    while mode==mode_pic:
        if time.perf_counter()-timer>duration: # time for next image
            index=(index+1)%len(imgs)
            timer=time.perf_counter() # reset stopwatch

        pixelsfill((0, 0, 0)) # clear screen
        for ball in range(balls):
            vy[ball]=gravity[ball]
            y[ball]+=vy[ball]
            if y[ball]>numy-1: 
                y[ball]=0
            setpixelHSV(int(round(x[ball],0)),int(round(y[ball],0)),hue[ball],0.1,0.5)#draw ball
        for y1 in range(16):
            for x1 in range(16):
                #r, g, b = imgs[index].getpixel((x, y))
                r, g, b = imgs[index].getpixel((x1, y1))
                if r>0 and g>0 and b>0:
                    setpixelRGB(x1,y1,(r,g,b))
        pixelsshow()

  
def textmode():
    unicode_text = u"  Merry Xmas"
    font = ImageFont.truetype("16x16font.ttf", 16, encoding="unic")
    text_width, text_height = font.getsize(unicode_text)
    #print(text_width, text_height )
    canvas = Image.new('RGB', (max(numx,text_width)+numx, max(numy,text_height) ), "black")
    draw = ImageDraw.Draw(canvas)
    draw.text((0,0), unicode_text, 'white', font)
    offset=0
    while offset<text_width:
        offset+=1
        pixelsfill((0, 0, 0)) # clear screen
        for y1 in range(numy):
            for x1 in range(numx):
                r, g, b = canvas.getpixel((x1+offset, y1))
                setpixelRGB(x1,y1,(r,g,b))
        pixelsshow()
        time.sleep(0.1)

# Define rotation matrices
def rotation_matrix_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotation_matrix_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotation_matrix_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def rotate_cube(cube, anglex, angley, anglez):
    output=np.dot(cube, rotation_matrix_x(anglex))
    output=np.dot(output, rotation_matrix_y(angley))
    output=np.dot(output, rotation_matrix_z(anglez))
    return output
    if axis == 'x':
        return np.dot(cube, rotation_matrix_x(angle))
    elif axis == 'y':
        return np.dot(cube, rotation_matrix_y(angle))
    elif axis == 'z':
        return np.dot(cube, rotation_matrix_z(angle))
    else:
        raise ValueError("Invalid rotation axis. Choose from 'x', 'y', or 'z'.")

def project_2d(points, focal_length=1):
    points[points[:, 2] == 0, 2] = 1e-6
    return points[:, :2] / (points[:, 2:3]+10)* focal_length

def draw_line(x1, y1, x2, y2, col):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            setpixelRGB(x,y,col)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            setpixelRGB(x,y,col)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    setpixelRGB(x,y,col)

def cube():
    vertices = np.array([
        [-1, -1, -1],   #left bottom    front   0 
        [-1, -1, 1],    #left bottom    back    1
        [-1, 1, -1],    #left top       front   2
        [-1, 1, 1],     #left top       back    3
        [1, -1, -1],    #right bottom   front   4
        [1, -1, 1],     #right bottom   back    5
        [1, 1, -1],     #right top      front   6
        [1, 1, 1]       #right top      back    7
    ])
    edges = [[0, 4], [4,6], [6,2], [2,0], [1,5], [5,7], [7,3], [3,1], [1,0], [3,2], [7,6], [5,4]]
    while mode==3:
        anglex = np.pi / 64
        angley = np.pi / 128 
        axis = 'y'  # rotate around y-axis
        #vertices = rotate_cube(vertices, angle, axis)
        vertices = rotate_cube(vertices, anglex, angley, 0)
        points_2d = project_2d(vertices)
        scaleup=35
        translate=7
        points_2d_scaled = [[round(i*scaleup+translate) for i in pnt] for pnt in points_2d]
        #print(points_2d_scaled)
        pixelsfill((0, 0, 0)) # clear screen
        
        for edge in edges:
            draw_line(points_2d_scaled[edge[0]][0],points_2d_scaled[edge[0]][1],points_2d_scaled[edge[1]][0],points_2d_scaled[edge[1]][1],(0,10,0))
        
        for pix in points_2d_scaled:
            setpixelRGB(pix[0],pix[1],(255,0,0))
        
        pixelsshow()
        time.sleep(0.1)
        #print(points_2d_scaled)
        #exit()

while True:
    mode=3
    #pong()
    cube()


