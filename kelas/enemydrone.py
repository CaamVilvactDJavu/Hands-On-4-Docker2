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


class enemydrone(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self, self.containers)
        (self.image, self.rect) = load_image('drone.png', 50,
                                             102, -1)
        self.rect.top = -self.rect.height
        self.rect.left = x

        self.cepat = 0
        self.tembak = 1
        self.gerak = [0, 0]
        self.nyawa = 20

        self.shot = False
        self.waitTime = 0
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
            ledakan(x, y, 100)
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def bedil(self):
        (x, y) = self.rect.center
        self.shot = pelurumusuh(x, y + self.rect.height / 2, (255, 0,
                                0), [0, 1], 10)
        self.shot = pelurumusuh(x, y + self.rect.height / 2, (255, 0,
                                0), [-0.5, 1], 10)
        self.shot = pelurumusuh(x, y + self.rect.height / 2, (255, 0,
                                0), [0.5, 1], 10)
        self.shot = pelurumusuh(x, y + self.rect.height / 2, (255, 0,
                                0), [-1, 1], 10)
        self.shot = pelurumusuh(x, y + self.rect.height / 2, (255, 0,
                                0), [1, 1], 10)

    def autopilot(self):
        if self.rect.top < height - 500:
            self.gerak[1] = 3
        elif self.rect.top > height - 500 and self.waitTime < 1000:
            self.gerak[1] = 0
            self.waitTime += 1

        if self.waitTime >= 150:
            self.gerak[1] = 5

        if self.rect.top > height:
            self.kill()
