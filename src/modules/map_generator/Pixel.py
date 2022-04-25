import pygame as pg
class pixel:
    def __init__(self, x:int, y:int):
        """
        args: (x:int, y:int) - the position of the pixel in the window
        """
        self.x = x
        self.y = y

    def draw(self, sc:pg.display, color=(255, 255, 255)):
        #draw a circle of radius 2 to represent one pixel in our map
        pg.draw.circle(sc, color, (self.x, self.y), 1)

    def __repr__(self) -> str:
        return f"self.x = {self.x}; self.y = {self.y}"