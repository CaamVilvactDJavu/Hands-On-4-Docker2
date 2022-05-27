import math
import sys
import time
import random
import os
import pygame

from pygame.locals import *
from load_image import load_image

from kelas.peluru import peluru

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


class player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        (self.image, self.rect) = load_image('pesawat.png', 72,
                                             72, -1)

        self.rect.top = size[1] - 100
        self.rect.left = size[0]/2

        self.cepat = 0
        self.tembak = 0
        self.gerak = [0, 0]
        self.pelatuk = 0
        self.nyawa = 200
        self.kills = 0
        self.skore = 0
        self.tundatembak = 0
        self.isautopilot = False
        self.shot = False
        self.won = False

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
        self.rect = self.rect.move(self.gerak)
        self.tundatembak += 1
        if self.tembak == 1 and self.tundatembak % 3 == 1:
            self.bedil()

        if self.nyawa > 200:
            self.nyawa = 200

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def bedil(self):
        (x, y) = self.rect.center
        self.shot = peluru(x - 14, y, (0, 255, 0), 1)
        self.shot = peluru(x + 14, y, (0, 255, 0), 1)

    def autopilot(self):
        if self.rect.centerx < width / 2:
            self.gerak[0] = 5
        else:
            self.gerak[0] = -5
        if self.rect.centerx - width / 2 < 5 and self.rect.centerx \
                - width / 2 > -5:
            self.gerak[0] = 0
            self.gerak[1] = -10
