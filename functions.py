"""
Script con funciones auxiliares.

Autores:
        - David Hernadez Rivera
        - J. Alfonso Martínez Baeza
        - M. Yvette Santana Sanchez
"""

import os # Permite ejecutar funciones del sistema operativo
import sys # Permite ejecutar funciones del sistema operativo
import random # Nos permite ejecutar funciones que requieren metodos aleatorios
import pygame # Conjunto de bibliotecas para diseñar juegos
import variables as var # Importamos las variables de un segundo archivo
import models as md # Importamos las clases para generar nuevos objetos

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
):
    """
    Funcion auxiliar para cargar imagenes
    """
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname).convert_alpha()
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        n_x,
        n_y,
        scalex=-1,
        scaley=-1,
        colorkey=None,
):
    """
    Funcion auxiliar para cargar hojas de sprites.
    """
    fullname = os.path.join('images', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert_alpha()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/n_x
    sizey = sheet_rect.height/n_y

    for i in range(0, n_y):
        for j in range(0, n_x):
            rect = pygame.Rect((j*sizex, i*sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert_alpha()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


def disp_game_over_msg(retbutton_image, game_over_image):
    """
    Muestra el mensaje de Game Over en pantalla.
    """
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = var.width / 2
    retbutton_rect.top = var.height*0.52

    game_over_rect = game_over_image.get_rect()
    game_over_rect.centerx = var.width / 2
    game_over_rect.centery = var.height*0.35

    var.screen.blit(retbutton_image, retbutton_rect)
    var.screen.blit(game_over_image, game_over_rect)


def extract_digits(number):
    """
    Extracción de los digitos del puntaje.
    """
    if number > -1:
        digits = []
        while number/10 != 0:
            digits.append(number % 10)
            number = int(number/10)

        digits.append(number % 10)
        for _ in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits

def introscreen():
    """
    Función para dibujar la pantalla de inicio
    """
    temp_goku = md.Goku(69, 72)
    temp_goku.is_blinking = True
    game_start = False

    logo, logo_rect = load_image('logo.png', 240, 159, -1)
    logo_rect.centerx = var.width*0.25
    logo_rect.centery = var.height*0.5

    callout, callout_rect = load_image('call_out.png', 300, 80, -1)
    callout_rect.left = var.width*0.5
    callout_rect.top = var.height*0.05

    shenron, shenron_rect = load_image('shenron.png', 325, 426, -1)
    shenron_rect.left = var.width*0.45
    shenron_rect.top = var.height*0.1

    while not game_start:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            return True

        for event in pygame.event.get():
            #esperando el evento de salir
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                # esperando el evento de teclado de espacio,
                # arriba y abajo para el movimiento del personaje
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    temp_goku.is_jumping = True
                    temp_goku.is_blinking = False
                    temp_goku.movement[1] = -1*temp_goku.jump_speed

        temp_goku.update()

        if pygame.display.get_surface() is not None:
            var.screen.fill(var.background_col)
            var.screen.blit(shenron, shenron_rect)
            if temp_goku.is_blinking:
                var.screen.blit(logo, logo_rect)
                var.screen.blit(callout, callout_rect)
            temp_goku.draw()

            pygame.display.update()

        var.clock.tick(var.FPS)
        if temp_goku.is_jumping is False and temp_goku.is_blinking is False:
            game_start = True


def gameplay():
    """
    En esta función se define el comportamiento de todos los objetos.
    """
    gamespeed = 5
    start_menu = False
    game_over = False
    game_quit = False
    player_goku = md.Goku(69, 72)
    new_ground = md.Ground(-1*gamespeed)
    scb = md.Scoreboard()
    highsc = md.Scoreboard(var.width*0.78)
    counter = 0

    saibamen = pygame.sprite.Group()
    energies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    md.Saibaman.containers = saibamen
    md.Energy.containers = energies
    md.Cloud.containers = clouds

    retbutton_image, _ = load_image(
        'replay_button.png', 35, 31, -1)
    game_over_image, _ = load_image('game_over.png', 190, 11, -1)

    temp_images, temp_rect = load_sprite_sheet(
        'numbers.png', 12, 1, 11, int(11*6/5), -1)
    hi_image = pygame.Surface((22, int(11*6/5)))
    hi_rect = hi_image.get_rect()
    hi_image.fill(var.violet)
    hi_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    hi_image.blit(temp_images[11], temp_rect)
    hi_rect.top = var.height*0.1
    hi_rect.left = var.width*0.73

    while not game_quit:
        while start_menu:
            pass
        while not game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            if player_goku.rect.bottom == int(0.98*var.height):
                                player_goku.is_jumping = True
                                if pygame.mixer.get_init() is not None:
                                    var.jump_sound.play()
                                player_goku.movement[1] = - \
                                    1*player_goku.jump_speed

                        if event.key == pygame.K_DOWN:
                            if not (player_goku.is_jumping and player_goku.is_dead):
                                player_goku.is_ducking = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player_goku.is_ducking = False
            for saibaman in saibamen:
                saibaman.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(player_goku, saibaman):
                    player_goku.is_dead = True
                    if pygame.mixer.get_init() is not None:
                        var.die_sound.play()

            for energy in energies:
                energy.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(player_goku, energy):
                    player_goku.is_dead = True
                    if pygame.mixer.get_init() is not None:
                        var.die_sound.play()

            if len(saibamen) < 2:
                if len(saibamen) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(md.Saibaman(gamespeed, 42, 44))
                else:
                    for obstacle in last_obstacle:
                        if obstacle.rect.right < var.width*0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(md.Saibaman(gamespeed, 42, 44))

            if len(energies) == 0 and random.randrange(0, 200) == 10 and counter > 500:
                for obstacle in last_obstacle:
                    if obstacle.rect.right < var.width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(md.Energy(gamespeed, 46, 40))

            if len(clouds) < 5 and random.randrange(0, 300) == 10:
                md.Cloud(var.width, random.randrange(var.height/5, var.height/2))

            player_goku.update()
            saibamen.update()
            energies.update()
            clouds.update()
            new_ground.update()
            scb.update(player_goku.score)
            highsc.update(var.HIGH_SCORE)

            if pygame.display.get_surface() is not None:
                var.screen.fill(var.background_col)
                new_ground.draw()
                clouds.draw(var.screen)
                scb.draw()
                if var.HIGH_SCORE != 0:
                    highsc.draw()
                    var.screen.blit(hi_image, hi_rect)
                saibamen.draw(var.screen)
                energies.draw(var.screen)
                player_goku.draw()

                pygame.display.update()
            var.clock.tick(var.FPS)

            if player_goku.is_dead:
                game_over = True
                if player_goku.score > var.HIGH_SCORE:
                    var.HIGH_SCORE = player_goku.score

            if counter % 700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if game_quit:
            break

        while game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_quit = True
                            game_over = False

                        if event.key == pygame.K_RETURN:
                            game_over = False
                            gameplay()
            highsc.update(var.HIGH_SCORE)
            if pygame.display.get_surface() is not None:
                disp_game_over_msg(retbutton_image, game_over_image)
                if var.HIGH_SCORE != 0:
                    highsc.draw()
                    var.screen.blit(hi_image, hi_rect)
                pygame.display.update()
            var.clock.tick(var.FPS)

    pygame.quit()
    sys.exit()


def main():
    """
    Función principal para iniciar el juego.
    """
    isgame_quit = introscreen()
    if not isgame_quit:
        gameplay()
