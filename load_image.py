import os
import pygame

from pygame.locals import *


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
