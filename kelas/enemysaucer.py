import math
import sys
import time
import random
import os
import pygame

from pygame.locals import *
from load_image import load_image

from kelas.ledakan import ledakan
from kelas.pelurumusuh import pelurumusuh


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


class enemysaucer(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('assets/images/saucer.png')
        self.images = []

        for i in range(0, 672, 96):
            rect = pygame.Rect((i, 0, 96, 96))
            image = pygame.Surface(rect.size)
            image = image.convert()
            colorkey = -1
            colorkey = image.get_at((10, 10))
            image.set_colorkey(colorkey, RLEACCEL)
            image.blit(sheet, (0, 0), rect)
            image = pygame.transform.scale(image, (48, 48))
            self.images.append(image)

        self.image = self.images[0]
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, -self.rect.height)
        self.nyawa = 10
        self.waitTime = 0
        self.tembak = 1
        self.gerak = [0, 0]
        self.haltpos = random.randrange(300, 510)
        self.shot = False
        self.ledakan_sound = \
            pygame.mixer.Sound('assets/audio/explosion.wav')
        self.ledakan_sound.set_volume(0.1)

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

        if self.tembak == 1 and self.waitTime % 10 == 1:
            self.bedil()

        if self.nyawa <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.ledakan_sound.play(maxtime=1000)
            ledakan(x, y, 75)
            self.kill()
        self.index += 1
        self.index = self.index % 7
        self.image = self.images[self.index]
        self.image = pygame.transform.rotate(self.image, 90)
        self.images[self.index] = self.image

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def bedil(self):
        (x, y) = self.rect.center
        self.shot = pelurumusuh(x, y, (0, 0, 255), [0, 1], 18)

    def autopilot(self):
        if self.rect.top < height - self.haltpos:
            self.gerak[1] = 3
        elif self.rect.top > height - self.haltpos and self.waitTime \
                < 1000:
            self.gerak[1] = 0
            self.waitTime += 1

        if self.waitTime >= 150:
            self.gerak[1] = 5

        if self.rect.top > height:
            self.kill()
