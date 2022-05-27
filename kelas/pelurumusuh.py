import math
import sys
import time
import random
import os
import pygame

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


class pelurumusuh(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        color,
        direction,
        cepat,
    ):

        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.col = list(color)
        for i in range(5, 0, -1):
            self.col[0] = color[0] * float(i) / 5
            self.col[1] = color[1] * float(i) / 5
            self.col[2] = color[2] * float(i) / 5
            pygame.draw.circle(self.image, tuple(self.col), (5, 5), i,
                               0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.cepat = cepat

    def update(self):
        (x, y) = self.rect.center
        y += self.direction[1] * self.cepat
        x += self.direction[0] * self.cepat
        self.rect.center = (x, y)
        if y <= 0 or y >= height or x <= 0 or x >= width:
            self.kill()
