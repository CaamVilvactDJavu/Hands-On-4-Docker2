import math
import sys
import time
import random
import os
import pygame

from pygame.locals import *
from kelas.bintang import bintang
from kelas.boss import boss
from kelas.enemydrone import enemydrone
from kelas.enemysaucer import enemysaucer
from kelas.kotaksehat import kotaksehat
from kelas.ledakan import ledakan
from kelas.musuh import musuh
from kelas.peluru import peluru
from kelas.pelurumusuh import pelurumusuh
from kelas.player import player
from load_image import load_image


size = (width, height) = (1024, 600)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (56, 49, 48)
green = (0, 155, 0)
red = (155, 0, 0)
sky = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 21
maxspeed = 15

screen = pygame.display.set_mode(size)


def cpumove(cpu, target):
    if target.rect.left < cpu.rect.left:
        cpu.pelatuk = 1
        cpu.cepat = -2
    elif target.rect.left > cpu.rect.left:
        cpu.pelatuk = 1
        cpu.cepat = 2
    if random.randrange(0, 30) == 1:
        cpu.tembak = 1
    else:
        cpu.tembak = 0


def bossmove(cpu, target):
    if target.rect.left < cpu.rect.left and cpu.spree == False:
        cpu.pelatuk = 1
        cpu.cepat = -2
    elif target.rect.left > cpu.rect.left and cpu.spree == False:
        cpu.pelatuk = 1
        cpu.cepat = 2

    if random.randrange(0, 3) == 1 and cpu.spree == False:
        cpu.bulletformation = 0
        cpu.bulletspeed = 20
        cpu.tembak = 1
    else:
        cpu.tembak = 0

    if cpu.spree == False and random.randrange(0, 250) == 71:
        cpu.spree = True
    else:
        pass


def showhealthbar(
    nyawa,
    barcolor,
    pos,
    unit,
):

    healthbar = pygame.Surface((nyawa * unit, 10), pygame.SRCALPHA, 32)
    healthbar = healthbar.convert_alpha()
    pygame.draw.rect(screen, barcolor, pos)


def displaytext(
    text,
    fontsize,
    x,
    y,
    color,
):

    font = pygame.font.SysFont('Fira Code', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)


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


def alurcerita(wavecounter):
    if wavecounter >= 0 and wavecounter <= 700:  # musuh
        return 0
    elif wavecounter > 700 and wavecounter <= 1100:  # saucer
        return 1
    elif wavecounter > 1100 and wavecounter <= 1500:  # drone
        return 2
    elif wavecounter > 1500 and wavecounter <= 1900:  # musuh and saucer
        return 3
    elif wavecounter > 1900 and wavecounter <= 2300:  # drone and saucer
        return 4
    elif wavecounter > 2300 and wavecounter <= 2700:  # musuh and drones
        return 5
    elif wavecounter > 2700:  # boss
        return 6


pygame.init()


def main():

    gameOver = False
    menuExit = False
    stageStart = False
    bossStage = False
    gameOverScreen = False

    menuselect = -1
    menuhighlight = 0

    wavecounter = 0
    wave = 0

    bntgjth1 = bintang(1, white, 50, 5)

    bullets = pygame.sprite.Group()
    enemybullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    drones = pygame.sprite.Group()
    saucers = pygame.sprite.Group()
    healthpacks = pygame.sprite.Group()

    peluru.containers = bullets
    pelurumusuh.containers = enemybullets
    musuh.containers = enemies
    ledakan.containers = explosions
    enemydrone.containers = drones
    enemysaucer.containers = saucers
    kotaksehat.containers = healthpacks

    user = player()
    pygame.display.set_caption('Space Battle')
    bg_music = pygame.mixer.Sound('assets/audio/bg_music1.ogg')
    boss_music = pygame.mixer.Sound('assets/audio/boss_music.ogg')

    (logoimage, logorect) = load_image('gamelogo1.png', -1, -1, -1)
    logorect.left = width / 2 - logorect.width / 2
    logorect.top = height / 2 - logorect.height * 5 / 4

    bg, bgrect = load_image('bg5.jpg')

    while not gameOver:
        while not menuExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menuExit = True
                    gameOver = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key \
                            == pygame.K_UP:
                        menuhighlight += 1
                    elif event.key == pygame.K_RETURN:
                        menuselect = menuhighlight % 2

            if menuselect == 0:
                stageStart = True
                menuExit = True
                bg_music.play(-1)
            elif menuselect == 1:
                pygame.quit()
                quit()
            else:
                pass

            screen.blit(bg, bgrect)
            bntgjth1.gambarbintang()

            user.drawplayer()
            screen.blit(logoimage, logorect)

            displaytext('Mulai', 32, width / 2 - 20, height * 3 / 4
                        - 40, white)
            displaytext('Keluar', 32, width / 2 - 20, height * 3 / 4,
                        white)

            if menuhighlight % 2 == 0:
                screen.blit(pygame.transform.scale(user.image, (25,
                            25)), [width / 2 - 100, height * 3 / 4
                            - 55, 15, 15])
            elif menuhighlight % 2 == 1:
                screen.blit(pygame.transform.scale(user.image, (25,
                            25)), [width / 2 - 100, height * 3 / 4
                            - 15, 15, 15])
            pygame.display.update()
            clock.tick(FPS)

        while stageStart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stageStart = False
                    gameOver = True
                if event.type == pygame.KEYDOWN:
                    user.pelatuk = 1
                    if event.key == pygame.K_LEFT:
                        user.cepat = -2
                    elif event.key == pygame.K_RIGHT:
                        user.cepat = 2
                    elif event.key == pygame.K_UP:
                        user.tembak = 1
                    elif event.key == pygame.K_ESCAPE:
                        quit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key \
                            == pygame.K_RIGHT:
                        user.pelatuk = 2
                        user.cepat = 0
                    if event.key == pygame.K_UP:
                        user.tembak = 0

            if wavecounter % 500 == 499 and random.randrange(0, 2) == 1 \
                    and len(healthpacks) < 1:
                kotaksehat(random.randrange(0, width - 50), 0, 10)

            if random.randrange(0, 8) == 1 and len(enemies) < 10 \
                    and (wave == 0 or wave == 3 or wave == 5 or wave == 6):
                musuh(random.randrange(0, 4))

            if random.randrange(0, 20) == 1 and len(saucers) < 3 \
                    and (wave == 1 or wave == 3 or wave == 4 or wave == 5):
                enemysaucer(random.randrange(0, width - 50))

            if random.randrange(0, 30) == 21 and len(drones) < 2 \
                    and (wave == 2 or wave == 3 or wave == 4):
                if len(drones) > 0:
                    for drone in drones:
                        if drone.rect.left < width / 2:
                            enemydrone(random.randrange(width / 2 + 60,
                                                        width - 60))
                        else:
                            enemydrone(random.randrange(0, width / 2
                                                        - 60))
                else:
                    enemydrone(random.randrange(0, width - 60))

            if wave == 6:
                bossStage = True
                stageStart = False
                finalboss = boss()
                user.nyawa += 80
                user.rect.left = width / 2
                user.rect.top = size[1] - 100
                user.isautopilot = False
                user.gerak = [0, 0]
                boss_music.play(-1)

            for ship in enemies:
                cpumove(ship, user)

            for musuhhit in pygame.sprite.groupcollide(enemies,
                                                       bullets, 0, 1):
                musuhhit.nyawa -= 1
                if musuhhit.nyawa <= 0:
                    user.kills += 1
                    user.skore += 1

            for dronehit in pygame.sprite.groupcollide(drones, bullets,
                                                       0, 1):
                dronehit.nyawa -= 1
                if dronehit.nyawa <= 0:
                    user.kills += 1
                    user.skore += 10

            for saucerhit in pygame.sprite.groupcollide(saucers,
                                                        bullets, 0, 1):
                saucerhit.nyawa -= 1
                if saucerhit.nyawa <= 0:
                    user.kills += 1
                    user.skore += 5

            for firedbullet in pygame.sprite.spritecollide(user,
                                                           enemybullets, 1):
                user.nyawa -= 1

            for enemycollided in enemies:
                if pygame.sprite.collide_mask(user, enemycollided):
                    user.nyawa -= 2
                    enemycollided.nyawa -= enemycollided.nyawa

            for dronecollided in drones:
                if pygame.sprite.collide_mask(user, dronecollided):
                    user.nyawa -= 10
                    dronecollided.nyawa -= dronecollided.nyawa

            for saucercollided in saucers:
                if pygame.sprite.collide_mask(user, saucercollided):
                    user.nyawa -= 4
                    saucercollided.nyawa -= saucercollided.nyawa

            for health_pack in healthpacks:
                if pygame.sprite.collide_mask(user, health_pack):
                    user.nyawa += health_pack.nyawa
                    health_pack.nyawa -= health_pack.nyawa

            if user.nyawa <= 0:
                gameOverScreen = True
                stageStart = False

            user.update()
            user.checkbounds()

            screen.blit(bg, bgrect)
            bntgjth1.gambarbintang()

            if user.nyawa > 0:
                showhealthbar(user.nyawa, red, [100, height - 20,
                              user.nyawa * 4, 10], 4)
            displaytext('Health', 22, 50, height - 15, white)
            displaytext('Score', 22, width - 100, 15, white)
            displaytext(str(user.skore), 22, width - 35, 15, white)
            user.drawplayer()

            enemies.update()
            bullets.update()
            enemybullets.update()
            explosions.update()
            drones.update()
            saucers.update()
            healthpacks.update()

            bullets.draw(screen)
            enemybullets.draw(screen)
            enemies.draw(screen)
            explosions.draw(screen)
            drones.draw(screen)
            saucers.draw(screen)
            healthpacks.draw(screen)

            wave = alurcerita(wavecounter)

            wavecounter += 1

            pygame.display.update()

            clock.tick(FPS)

            moveplayer(user)

            print(
                wavecounter,
                wave,
                user.kills,
                user.nyawa,
                user.rect.left,
                user.gerak[0],
                user.rect.right,
            )

        while bossStage:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                    bossStage = False
                if event.type == pygame.KEYDOWN:
                    user.pelatuk = 1
                    if event.key == pygame.K_LEFT:
                        user.cepat = -2
                    elif event.key == pygame.K_RIGHT:
                        user.cepat = 2
                    elif event.key == pygame.K_UP:
                        user.tembak = 1
                    elif event.key == pygame.K_ESCAPE:
                        quit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key \
                            == pygame.K_RIGHT:
                        user.pelatuk = 2
                        user.cepat = 0
                    if event.key == pygame.K_UP:
                        user.tembak = 0

            bossmove(finalboss, user)

            for ship in enemies:
                cpumove(ship, user)

            for userbullet in bullets:
                if pygame.sprite.collide_mask(finalboss, userbullet):
                    if finalboss.nyawa > 2:
                        finalboss.nyawa -= 1
                    else:
                        bossStage = False
                        gameOverScreen = True
                        user.skore += 200
                        user.won = True
                    userbullet.kill()

            for musuhhit in pygame.sprite.groupcollide(enemies,
                                                       bullets, 0, 1):
                musuhhit.nyawa -= 1
                if musuhhit.nyawa <= 0:
                    user.kills += 1
                    user.skore += 1

            for dronehit in pygame.sprite.groupcollide(drones, bullets,
                                                       0, 1):
                dronehit.nyawa -= 1
                if dronehit.nyawa <= 0:
                    user.kills += 1
                    user.skore += 10

            for saucerhit in pygame.sprite.groupcollide(saucers,
                                                        bullets, 0, 1):
                saucerhit.nyawa -= 1
                if saucerhit.nyawa <= 0:
                    user.kills += 1
                    user.skore += 5

            for firedbullet in pygame.sprite.spritecollide(user,
                                                           enemybullets, 1):
                user.nyawa -= 1

            for musuhcollided in enemies:
                if pygame.sprite.collide_mask(user, musuhcollided):
                    user.nyawa -= 2
                    musuhcollided.nyawa -= musuhcollided.nyawa

            for dronecollided in drones:
                if pygame.sprite.collide_mask(user, dronecollided):
                    user.nyawa -= 10
                    dronecollided.nyawa -= dronecollided.nyawa

            for saucercollided in saucers:
                if pygame.sprite.collide_mask(user, saucercollided):
                    user.nyawa -= 4
                    saucercollided.nyawa -= saucercollided.nyawa

            if user.nyawa <= 0:
                gameOverScreen = True
                bossStage = False

            user.update()
            user.checkbounds()

            screen.blit(bg, bgrect)
            bntgjth1.gambarbintang()

            if user.nyawa > 0:
                showhealthbar(user.nyawa, green, [100, height - 20,
                              user.nyawa * 4, 10], 4)
            displaytext('HEALTH', 22, 50, height - 15, white)

            if finalboss.nyawa > 0:
                showhealthbar(finalboss.nyawa, red, [100, 20,
                              finalboss.nyawa * 0.8, 10], 0.8)
            displaytext('BOSS', 22, 50, 25, white)

            displaytext('Score:', 22, width - 100, 15, white)
            displaytext(str(user.skore), 22, width - 35, 15, white)

            user.drawplayer()

            enemies.update()
            bullets.update()
            enemybullets.update()
            drones.update()
            saucers.update()
            explosions.update()
            finalboss.update()

            bullets.draw(screen)
            enemybullets.draw(screen)
            enemies.draw(screen)
            drones.draw(screen)
            saucers.draw(screen)
            explosions.draw(screen)
            finalboss.drawplayer()

            pygame.display.update()
            clock.tick(FPS)
            moveplayer(user)

        while gameOverScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOverScreen = False
                    gameOver = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameOverScreen = False
                    gameOver = True

            screen.fill(sky)
            bntgjth1.gambarbintang()

            if user.won == False:
                displaytext('Game Berakhir', 26, width / 2 - 30, height
                            / 2, white)
            else:
                displaytext('Selamat! Kamu Menang!', 26, width / 2
                            - 30, height / 2, white)

            displaytext('Score kamu : ', 26, width / 2 - 40, height / 2
                        + 40, white)
            displaytext(str(user.skore), 26, width / 2 + 50, height / 2
                        + 43, white)
            displaytext('Tekan Enter untuk keluar...', 14, width / 2 - 30,
                        height / 2 + 90, white)
            pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
