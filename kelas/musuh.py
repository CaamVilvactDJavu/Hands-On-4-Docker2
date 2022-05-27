import math
import sys
import time
import random
import os
import pygame

from pygame.locals import *
from load_image import load_image

from kelas.pelurumusuh import pelurumusuh
from kelas.ledakan import ledakan


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


def moveplayer(Player):
    if Player.isautopilot == False:
        if Player.rect.left >= 0 and Player.rect.right <= width:
            if Player.pelatuk == 1:
                Player.gerak[0] = Player.gerak[0] + Player.cepat
                if Player.gerak[0] < -maxspeed:
                    Player.gerak[0] = -maxspeed
                elif Player.gerak[0] > maxspeed:
                    Player.gerak[0] = maxspeed
            elif Player.gerak[0] >= -maxspeed and Player.gerak[0] \
                    < 0 and Player.pelatuk == 2:
                Player.gerak[0] += math.fabs(Player.gerak[0] / 20)
                if Player.gerak[0] > 0:
                    Player.gerak[0] = 0
            elif Player.gerak[0] <= maxspeed and Player.gerak[0] \
                    > 0 and Player.pelatuk == 2:
                Player.gerak[0] -= math.fabs(Player.gerak[0] / 20)
                if Player.gerak[0] < 0:
                    Player.gerak[0] = 0
    else:
        Player.autopilot()


class musuh(pygame.sprite.Sprite):

    def __init__(self, n=0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('assets/images/enemy_musuh.png')
        self.images = []

        rect = pygame.Rect((0, 0, 85, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((86, 0, 71, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((158, 0, 68, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((227, 0, 65, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        self.image = self.images[n]
        self.image = self.image.convert()
        colorkey = -1
        colorkey = self.image.get_at((10, 10))
        self.image.set_colorkey(colorkey, RLEACCEL)

        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, 180)
        self.rect.top = 0
        self.rect.left = random.randrange(0, width - 72)

        self.cepat = 0
        self.tembak = 0
        self.gerak = [0, 0]
        self.pelatuk = 0
        self.nyawa = 2
        self.isautopilot = False

        self.ledakan_sound = \
            pygame.mixer.Sound('assets/audio/explosion.wav')
        self.ledakan_sound.set_volume(0.1)

        self.shot = False

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

        moveplayer(self)
        self.autopilot()
        self.rect = self.rect.move(self.gerak)

        if self.tembak == 1:
            self.bedil()

        if self.nyawa <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.ledakan_sound.play(maxtime=1000)
            ledakan(x, y)
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def bedil(self):
        (x, y) = self.rect.center
        self.shot = pelurumusuh(x, y, (255, 255, 0), [0, 1], 12)

    def autopilot(self):
        if self.rect.top < height:
            self.gerak[1] = 5
        else:
            self.kill()
