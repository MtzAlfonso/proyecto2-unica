"""
Autores:
        - David Hernadez Rivera
        - J. Alfonso Martínez Baeza
        - M. Yvette Santana Sanchez
"""
import random #funciones relacionadas con los valores aleatorios
import pygame # Conjunto de bibliotecas para diseñar juegos
import variables as var #Importamos las variables del archivo variables
import functions as fn #Importamos las funciones del archivo fn

class Goku():
    """
    
    """
    def __init__(self, sizex=-1, sizey=-1):
        self.images, self.rect = fn.load_sprite_sheet(
            'goku_3.png', 5, 1, sizex, sizey, -1)
        self.images1, self.rect1 = fn.load_sprite_sheet(
            'dino_ducking.png', 2, 1, 59, sizey, -1)
        self.rect.bottom = int(0.98*var.height)
        self.rect.left = var.width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.is_jumping = False
        self.is_dead = False
        self.is_ducking = False
        self.is_blinking = False
        self.movement = [0, 0]
        self.jump_speed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        """
        """
        var.screen.blit(self.image, self.rect)

    def checkbounds(self):
        """
        """
        if self.rect.bottom > int(0.98*var.height):
            self.rect.bottom = int(0.98*var.height)
            self.is_jumping = False

    def update(self):
        """
        """
        #estado del objeto, puede estar saltando o no
        if self.is_jumping:
            self.movement[1] = self.movement[1] + var.GRAVITY
            #si esta saltando la gravedad afecta al movimiento de personaje

        if self.is_jumping:
            self.index = 4
            #cuando se esta agachando tenemos lo siguientes factores que afectan al personaje
        elif self.is_blinking:
            if self.index == 4:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.is_ducking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.is_dead:
            self.index = 4

        if not self.is_ducking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width+10
        else:
            self.image = self.images1[(self.index) % 2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.is_dead and self.counter % 7 == 6 and not self.is_blinking:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() is not None:
                    var.checkpoint_sound.play()

        self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = fn.load_sprite_sheet(
            'saibamen.png', 5, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98*var.height)
        self.rect.left = var.width + self.rect.width
        self.image = self.images[random.randrange(0, len(self.images))]
        self.movement = [-1*speed, 0]

    def draw(self):
        var.screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class Energy(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = fn.load_sprite_sheet(
            'ptera.png', 2, 1, sizex, sizey, -1)
        self.ptera_height = [var.height*0.9, var.height*0.8, var.height*0.7]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = var.width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        """
        """
        var.screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class Ground():
    def __init__(self, speed=-5):
        self.image, self.rect = fn.load_image('fondo_kaio.png', -1, -1, -1)
        self.image1, self.rect1 = fn.load_image('fondo_kaio.png', -1, -1, -1)
        self.rect.bottom = var.height
        self.rect1.bottom = var.height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        var.screen.blit(self.image, self.rect)
        var.screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = fn.load_image('cloud.png', int(90*30/42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed, 0]

    def draw(self):
        var.screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = fn.load_sprite_sheet(
            'numbers.png', 12, 1, 11, int(11*6/5), -1)
        self.image = pygame.Surface((55, int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = var.width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = var.height*0.1
        else:
            self.rect.top = y

    def draw(self):
        var.screen.blit(self.image, self.rect)

    def update(self, score):
        score_digits = fn.extract_digits(score)
        self.image.fill(var.background_col)
        for digits in score_digits:
            self.image.blit(self.tempimages[digits], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0
