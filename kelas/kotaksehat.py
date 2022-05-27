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


class kotaksehat(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        nyawa,
    ):

        pygame.sprite.Sprite.__init__(self, self.containers)
        self.nyawa = nyawa
        (self.image, self.rect) = load_image(
            'healthpack1.png', 40, 40, -1)
        self.rect.left = x
        self.rect.top = y
        self.gerak = [3, 0]
        self.maxleft = self.rect.left - 20
        self.maxright = self.rect.right + 20

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.gerak[0] = 0
            self.cepat = 0
        if self.rect.right > width:
            self.rect.right = width
            self.gerak[0] = 0
            self.cepat = 0

    def update(self):
        self.checkbounds()
        self.autopilot()
        self.rect = self.rect.move(self.gerak)

        if self.nyawa <= 0 or self.rect.top > height:
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def autopilot(self):
        if self.rect.right > self.maxright:
            self.gerak[0] = -3
        elif self.rect.left < self.maxleft:
            self.gerak[0] = 3

        self.gerak[1] = 5
