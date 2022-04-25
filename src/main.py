#import modules
import pygame
from modules.map_reader.rgb import get_rgb
from PIL import Image
import json
import numpy as np

#global variables
screensize = (1000, 1000)
imgsize = (1000, 1000)
imgcolors = []
food_coordinates = ()

#load variables from JSON
with open("screenshot.json", 'r') as file:
    data = json.loads(file.read())
    imgcolors = data["pixels"]
    food_coordinates = data["food_coordinates"]
    pixelsthrow = imgcolors
    pixelsthrow[food_coordinates[0]][food_coordinates[1]] = (0, 255, 0)
    Image.fromarray(np.asarray(pixelsthrow), 'RGB').save('screenshot.jpg')


#screen
screen = pygame.display.set_mode(screensize)
background = pygame.image.load("screenshot.jpg")

#ant class
from random import randint

ants = []

class ant():
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y
        if x == -1:
            self.x = randint(0, screensize[0])
        if y == -1:
            self.y = randint(0, screensize[1])
    def __repr__(self):
        return f"self.x:{self.x}; self.y:{self.y}"
    def nextmove(self):
        """
        decide where to go depending on where the walls are. Completely random for now
        """
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        if possiblemove((self.x+dx, self.y+dy)):
            self.x+=dx
            self.y+=dy
    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 2)

for _ in range(50):
    ants.append(ant())


def possiblemove(coor):
    if coor[0] < 0 or coor[1] < 0 or coor[0] > screensize[0] or coor[1] > screensize[1] or coor[0] >= imgsize[0] or coor[1] >= imgsize[1]:
        return False
    return imgcolors[coor[0]][coor[1]] == (0, 0, 0)
    

clock = pygame.time.Clock()

while True:
    #input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for a in ants:
        a.nextmove()
        a.draw()
    pygame.display.update()
    clock.tick(120)
    