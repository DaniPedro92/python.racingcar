import pygame
from configs import *
from car import My_car
import random
import time
from cpu_car import CPU_car
from race_conditions import *

pygame.init()

screen = pygame.display.set_mode([window.WIDTH, window.HEIGHT])
pygame.display.set_caption(window.TITLE)
pygame.display.set_icon(window.ICON)

#pygame.time.delay(1000)

PATH = [(243, 190), (212, 139), (137, 144), (107, 206), (139, 250), (93, 350), (140, 454), (104, 578), (346, 784), (417, 875), (507, 836), (506, 621), (612, 560), (703, 609), (704, 816), (793, 878), (882, 838), (865, 502), (821, 449), (542, 460), (495, 437), (494, 356), (563, 332), (834, 329), (883, 284), (875, 189), (801, 128), (399, 132), (350, 188), (355, 438), (365, 488), (300, 522), (233, 466), (240, 306)]

img.load_images()

player_car = My_car(4, 4, 220, 245)
cpu_car = CPU_car(2, 3, 250, 245, PATH) 

barrier_positions = [
    [80, 250],
    [129, 350],
    [80, 450],
    [883, 717],
    [833, 579],
    [209, 350],
    [258, 420],
    [323, 410],
    [372, 300],
]
oil_positions = [
    [300, 800],
    [138, 550],
    [490, 600]
]
boost_positions = [
    [150, 635],
    [860, 715],
    [750, 450],
    [590, 340],
    [750, 125],
    [350, 240],
    [240, 390],
]
checkpoints_positions = [
    [80, 200],
    [80, 500],
    [463, 750],
    [678, 750],
    [833, 750],
    [833, 550],
    [833, 220],
    [324, 220],
    [324, 420],
    [460, 390],
]

pit_stop_positions = [
    [611, 114],
    [560, 560],
]

in_menu = True

def draw_button(image, x, y, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    image_rect = image.get_rect(topleft=(x, y))

    if image_rect.collidepoint(mouse):
        if click[0] == 1 and action is not None:
            action()
    screen.blit(image, image_rect) 

def start_game():
    global show_menu
    show_menu = False

def quit_game():
    pygame.quit()
    exit()

show_menu = True

while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(img.BACKGROUND, (0, 300))

    draw_button(img.START, 100, 600, start_game)
    draw_button(img.EXIT, 550, 600, quit_game)

    pygame.display.update()

def show_lights_sequence():
    global lights_index, lights_last_time, show_lights

    if show_lights:
        current_time = pygame.time.get_ticks()

        if current_time - lights_last_time >= lights_duration:
            lights_last_time = current_time
            lights_index += 1
            if lights_index >= len(img.LIGHTS_SURFACES):
                show_lights = False 

        if show_lights: 
            screen.blit(img.LIGHTS_SURFACES[lights_index], (window.WIDTH / 2 - img.LIGHTS_SURFACES[lights_index].get_width() / 2, window.HEIGHT / 4 - img.LIGHTS_SURFACES[lights_index].get_height() / 2))
            pygame.display.update()

lights_index = 0
lights_duration = 1000  
lights_last_time = 0
show_lights = True

sound.STARTING_LIGHTS.play(maxtime=4000)

while show_lights:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    show_lights_sequence()
    pygame.time.delay(10)



boost_timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(boost_timer_event, 2000)

victory_message_duration = 3000
loser_message_duration = 3000 
victory_time = 0
victory_message_visible = False
loser_message_visible = False
loser_message_display_time = 0

checkpoints_positions = [(x, y) for x, y in checkpoints_positions]
checkpoints_passed = set()
crossed_finish_line = False
player_car.checkpoints_passed = set()
cpu_car.checkpoints_passed = set() 

current_boosts = []

finish_message_visible = False
finish_message_time = 0
finish_image_duration = 20000

paused = False

run = True
clock = pygame.time.Clock()

while run:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
        if event.type == boost_timer_event:
            player_car.max_vel = 4
            current_boosts = random.sample(boost_positions, 3)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
    
    if not paused:    
        cpu_car.move()
        check_checkpoints_and_finish(player_car, checkpoints_positions, 206, 300)
        check_checkpoints_and_finish(cpu_car, checkpoints_positions, 206, 300)
        
        key = pygame.key.get_pressed()
        moved = False

        if key[pygame.K_LEFT]:
            player_car.rotate(left=True)
        elif key[pygame.K_RIGHT]:
            player_car.rotate(right=True)

        if key[pygame.K_UP]:
            moved = True
            player_car.move_forward()
        
        if player_car.collide_with(img.TRACK_BORDER_MASK, 50, 50):
            player_car.take_damage(0.3)
            player_car.vel = 0.5
            
        for barrier_position in barrier_positions:
            barrier_x, barrier_y = barrier_position
            if player_car.collide_with(img.BARRIER_MASK, barrier_x, barrier_y) > 0:
                player_car.take_damage(0.3)
                player_car.rebound()
                
        for oil_position in oil_positions:
            oil_x, oil_y = oil_position
            if player_car.collide_with(img.OIL_MASK, oil_x, oil_y):
                player_car.spin_out()

        for pit_stop_position in pit_stop_positions:
            pit_stop_x, pit_stop_y = pit_stop_position
            if player_car.collide_with(img.PIT_STOP_MASK, pit_stop_x, pit_stop_y):
                player_car.health = player_car.health_max

        for boost_position in current_boosts:
            boost_x, boost_y = boost_position
            if player_car.collide_with(img.BOOST_MASK, boost_x, boost_y):
                player_car.boost()
                pygame.time.set_timer(boost_timer_event, 1000)

        for pos in checkpoints_positions:
            if player_car.collide_with(img.CHECKPOINT_MASK, pos[0], pos[1]) > 0:
                checkpoints_passed.add(pos)

        for pos in checkpoints_positions:
            if cpu_car.collide_with(img.CHECKPOINT_MASK, pos[0], pos[1]) > 0:
                cpu_car.checkpoints_passed.add(pos)

        if len(checkpoints_passed) == len(checkpoints_positions):
            if player_car.collide_with(img.FINISH_MASK, 206, 300) > 0:
                crossed_finish_line = True
            else:
                crossed_finish_line = False
        else:
            crossed_finish_line = False

        if len(cpu_car.checkpoints_passed) == len(checkpoints_positions) and cpu_car.collide_with(img.FINISH_MASK, 206, 300) > 0:
            cpu_car.crossed_finish_line = True
        else:
            cpu_car.crossed_finish_line = False

        if cpu_car.crossed_finish_line and not finish_message_visible:
            finish_message_visible = True
            screen.blit(img.FINISH_IMAGE, (window.WIDTH // 2 - img.FINISH_IMAGE.get_width() // 2, window.HEIGHT // 2 - img.FINISH_IMAGE.get_height() // 2))
            finish_message_time = pygame.time.get_ticks()

        if finish_message_visible:
            screen.blit(img.FINISH_IMAGE, (window.WIDTH // 2 - img.FINISH_IMAGE.get_width() // 2, window.HEIGHT // 2 - img.FINISH_IMAGE.get_height() // 2))
            if pygame.time.get_ticks() - finish_message_time >= finish_image_duration:
                finish_message_visible = False

        if player_car.collide_with(img.FINISH_MASK, 206, 300) > 0:
            crossed_finish_line = True

        if player_car.crossed_finish_line:
            if not victory_message_visible:
                victory_time = pygame.time.get_ticks()
                victory_message_visible = True

        if victory_message_visible and pygame.time.get_ticks() - victory_time >= victory_message_duration:
            show_victory_screen()
            pygame.time.delay(victory_message_duration + 4000) 
            victory_message_visible = False
            pygame.quit()
            exit()

        if cpu_car.crossed_finish_line:
            if not loser_message_visible:
                loser_time = pygame.time.get_ticks()
                loser_message_visible = True

        if loser_message_visible and pygame.time.get_ticks() - loser_time >= loser_message_duration:
            show_loser_screen()
            pygame.time.delay(loser_message_duration + 4000) 
            loser_message_visible = False
            pygame.quit()
            exit()

        if key[pygame.K_SPACE]: 
            if player_car.vel > 0:
                player_car.vel -= 0.2

        if not moved:
            player_car.reduce_vel()

        if key[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

        screen.blit(img.GRASS, [0, 0])
        screen.blit(img.TRACK, [50, 50])
        screen.blit(img.FINISH_RESIZE, [206, 300])
        screen.blit(img.TRACK_BORDER, [50, 50])
        
        
        for pos in barrier_positions:
            screen.blit(img.BARRIER, pos)
        for pos in oil_positions:
            screen.blit(img.OIL, pos)
        for pos in current_boosts:  
            screen.blit(img.BOOST, pos)
        for pos in checkpoints_positions:
            screen.blit(img.CHECKPOINT, pos)
        for pos in pit_stop_positions:
            screen.blit(img.PIT_STOP, pos)

        player_car.draw(screen)
        cpu_car.draw(screen)

        pygame.draw.rect(screen, (128, 128, 128), (50 - 5, 20 - 5, 100 + 10, 10 + 10), border_radius=5)
        pygame.draw.rect(screen, (0, 255, 0), (50, 20, player_car.health, 10))
        pygame.draw.rect(screen, (255, 0, 0), (50 + player_car.health, 20, 100 - player_car.health, 10))

        health_percentage = int(player_car.health)
        text = pygame.font.Font(None, 25).render(f"Health: {health_percentage}%", True, (255, 255, 255))
        screen.blit(text, (160, 18))

        font = pygame.font.Font(None, 30)
        speed_surface = font.render(f"Speed: {(player_car.vel * 100):.1f} km/h", True, (255, 255, 255))
        screen.blit(speed_surface, (window.WIDTH - speed_surface.get_width() - 20, window.HEIGHT - speed_surface.get_height() - 20))
        
        if len(checkpoints_passed) == len(checkpoints_positions) and crossed_finish_line and not finish_message_visible:
            finish_message_visible = True
            screen.blit(img.FINISH_IMAGE, (window.WIDTH // 2 - img.FINISH_IMAGE.get_width() // 2, window.HEIGHT // 2 - img.FINISH_IMAGE.get_height() // 2))
            finish_message_time = pygame.time.get_ticks()
        
        if finish_message_visible:
            show_finish_message_screen()
            if pygame.time.get_ticks() - finish_message_time >= finish_image_duration:
                finish_message_visible = False

        pygame.display.update()

pygame.quit()
