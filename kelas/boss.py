import math
import sys
import time
import random
import os
import pygame

from pygame.locals import *
from load_image import load_image

from kelas.enemysaucer import enemysaucer
from kelas.musuh import musuh
from kelas.pelurumusuh import pelurumusuh
from kelas.enemydrone import enemydrone


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


class boss(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        (self.image, self.rect) = load_image('bossx.png', 200, 400, -1)
        self.rect = self.image.get_rect()
        self.rect.top = 100
        self.rect.left = random.randrange(0, width - 72)

        self.cepat = 0
        self.tembak = 0
        self.gerak = [0, 0]
        self.pelatuk = 0
        self.nyawa = 600
        self.bulletformation = 0
        self.bulletspeed = 20
        self.spreecount = 0
        self.spree = False
        self.shot = False
        self.isautopilot = False
        self.reloadtime = 0

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

        self.rect = self.rect.move(self.gerak)

        if self.tembak == 1 and self.reloadtime == 0:
            self.bedil(self.bulletformation, self.bulletspeed)

        if self.reloadtime > 0:
            self.reloadtime -= 1

        if self.nyawa <= 0:
            self.kill()

        if self.spree == True and self.spreecount <= 70:
            self.spreecount += 1
            if self.spreecount % 5 == 1:
                self.gerak[0] = 0
                self.cepat = 0
                self.bedil(1, 10)
            else:
                pass
        else:
            self.spree = False
            self.spreecount = 0

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def bedil(self, bulletformation=0, bulletspeed=20):
        (x, y) = self.rect.center
        if bulletformation == 0:
            self.shot = pelurumusuh(x, y + self.rect.height / 2, (255,
                                    0, 255), [0, 1], bulletspeed)
            self.shot = pelurumusuh(x - self.rect.width / 2 + 30, y
                                    - self.rect.height / 2 + 50, (255,
                                                                  0, 255), [0, 1], bulletspeed)
            self.shot = pelurumusuh(x + self.rect.width / 2 - 30, y
                                    - self.rect.height / 2 + 50, (255,
                                                                  0, 255), [0, 1], bulletspeed)
        elif bulletformation == 1:
            self.shot = pelurumusuh(x, y, (255, 0, 255), [1.5, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [-1.5, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [1.2, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [-1.2, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [0, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [0.9, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [-0.9, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [0.6, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [-0.6, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [0.3, 1],
                                    bulletspeed)
            self.shot = pelurumusuh(x, y, (255, 0, 255), [-0.3, 1],
                                    bulletspeed)

        if random.randrange(0, 10) == 4:
            musuh(random.randrange(0, 4))
        if random.randrange(0, 50) == 41:
            enemysaucer(random.randrange(0, width - 50))
        if random.randrange(0, 200) == 121:
            enemydrone(random.randrange(0, width - 50))
