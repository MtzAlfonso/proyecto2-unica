"""
Autores:
        - David Hernadez Rivera
        - J. Alfonso Martínez Baeza
        - M. Yvette Santana Sanchez
"""
#importamos el modulo que necesitamos para realizar este juego
import pygame
#siempre hacemos una mencion a  init para utilizar la importancion de pygame
pygame.init()

#damos propiedades al audio
pygame.mixer.pre_init(44100, -16, 2, 2048)

#definimos las  proporciones de la pantalla
scr_size = (width, height) = (720, 350)
#constantes que vamos a utilizar a lo largo del codigo
FPS = 40
GRAVITY = 0.6
HIGH_SCORE = 0
black = (0, 0, 0)
white = (255, 255, 255)
background_col = (218, 126, 0)

#creamos una ventana que recibe las proporciones anteriores
screen = pygame.display.set_mode(scr_size)
#utilizamos clock para las horas
clock = pygame.time.Clock()
#colocamos un mensaje en pantalla
pygame.display.set_caption("DBZ - El camino de la serpiente")
#colocamos la imagen del dragon en pantalla, usamos ALPHA para png
shenron = pygame.image.load("images/shenron.png").convert_alpha()

#cargamos los sonidos que vamos a utilizar en nuestro juego con MIXER
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
die_sound = pygame.mixer.Sound('sounds/die.wav')
checkpoint_sound = pygame.mixer.Sound('sounds/checkPoint.wav')
