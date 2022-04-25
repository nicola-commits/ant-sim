#import libraries
# sourcery skip: merge-nested-ifs
import contextlib
import itertools
import pygame as pg
import time
from Line import bresenham
from Pixel import pixel
import json

#global variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pixels = []
last = 0
erasersize = 16
lasteraser = (0, 0)
screenshot = False
foodcoor = False
screensize = (1000, 1000)
pixdict = [[(0, 0, 0) for _ in range(screensize[0])] for _ in range(screensize[1])]


#create a screen
screen = pg.display.set_mode(screensize)

#create a clock
clock = pg.time.Clock()

while True:
    screen.fill((0, 0, 0))

    #event handler
    for event in pg.event.get():

        #if the user wants to quit, quit
        if event.type == pg.QUIT:
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                foodcoor = pg.mouse.get_pos()

        #check for mouse clicks
        #using the function
        #pg.mouse.get_pressed() will return a list of booleans
        #representing left, wheel and right click respectively
        pressedbuttons = pg.mouse.get_pressed()
        #only go on if any mouse button is pressed

        if any(pressedbuttons):

            #record the coordinates
            coord = pg.mouse.get_pos()

            #if left click
            if pressedbuttons[0]:
                #if the delay between one click and the other one is exactly one frame,
                #draw a line that connects the two
                if time.time() - last < 1/20:
                    #if the two pixels are basically identical, continue
                    if pixels[-1].x != coord[0] or pixels[-1].y != coord[1]:
                        #new code (bresenham algorithm)
                        for item in bresenham(pixels[-1].x, pixels[-1].y, coord[0], coord[1]):
                            p = pixel(item[0], item[1])
                            pixdict[coord[0]][coord[1]] = (255, 255, 255)
                            pixels.append(p)
                else:

                    #as with minecraft, left click will place a pixel
                    p = pixel(coord[0], coord[1])
                    pixdict[coord[0]][coord[1]] = (255, 255, 255)
                    pixels.append(p)

            #if right click
            if pressedbuttons[2]:
                #destroy the pixel selected
                if time.time() - last < 1/20:
                    for c, p in itertools.product(bresenham(lasteraser[0], lasteraser[1], coord[0], coord[1]), pixels):
                        if p.x in range(-erasersize+c[0], erasersize+c[0]) and p.y in range(-erasersize+c[1], erasersize+c[1]):
                            with contextlib.suppress(Exception):
                                pixels.remove(p)
                else:
                    for p in pixels:
                        if p.x in range(-erasersize+coord[0], erasersize+coord[0]) and p.y in range(-erasersize+coord[1], erasersize+coord[1]):
                            pixels.remove(p)
                #set last eraser
                lasteraser = coord

            if pressedbuttons[1]:
                screenshot = True

            last = time.time()


    #draw the pixels
    for p in pixels:
        p.draw(screen)

    if foodcoor:
        pg.draw.circle(screen, (0, 255, 0), (foodcoor[0], foodcoor[1]), 1)

    if screenshot:
        p = {"pixels":pixdict, "food_coordinates":foodcoor}
        with open("screenshot.json", "w") as infile:
            infile.write(json.dumps(p))
        screenshot = False

    pg.display.update()
    #os.system('cls' if os.name == 'nt' else 'clear')

    