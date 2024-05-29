import pygame
from configs import *

pygame.init()
screen = pygame.display.set_mode([window.WIDTH, window.HEIGHT])

def show_finish_message_screen():
    screen.blit(img.FINISH_IMAGE, (window.WIDTH // 2 - img.FINISH_IMAGE.get_width() // 2, window.HEIGHT // 2 - img.FINISH_IMAGE.get_height() // 2))

def show_victory_screen():
    screen.blit(img.VICTORY, (50, 50))
    pygame.display.update()

def show_loser_screen():
    screen.blit(img.LOSER, (50, 50))
    pygame.display.update()

def check_checkpoints_and_finish(car, checkpoints, finish_x, finish_y):
    for pos in checkpoints:
        if car.collide_with(img.CHECKPOINT_MASK, pos[0], pos[1]) > 0:
            car.checkpoints_passed.add(pos)

    if len(car.checkpoints_passed) == len(checkpoints):
        if car.collide_with(img.FINISH_MASK, finish_x, finish_y) > 0:
            car.crossed_finish_line = True
        else:
            car.crossed_finish_line = False
    else:
        car.crossed_finish_line = False

