import math
import sys
import time
import random
import os
import pygame

from pygame.locals import *
from load_image import load_image

size = (width, height) = (1024, 600)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 155, 0)
red = (155, 0, 0)
sky = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 21
maxspeed = 15

screen = pygame.display.set_mode(size)


def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
):

    fullname = os.path.join('assets/images', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())


class ledakan(pygame.sprite.Sprite):

    def __init__(self, x, y, radius=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('assets/images/ledakan.png')
        self.images = []
        for i in range(0, 768, 48):
            rect = pygame.Rect((i, 0, 48, 48))
            image = pygame.Surface(rect.size)
            image = image.convert()
            colorkey = -1
            colorkey = image.get_at((10, 10))
            image.set_colorkey(colorkey, RLEACCEL)

            image.blit(sheet, (0, 0), rect)
            if radius != -1:
                image = pygame.transform.scale(image, (radius, radius))
            self.images.append(image)

        self.image = self.images[0]
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.image = self.images[self.index]
        self.index += 1
        if self.index >= len(self.images):
            self.kill()
