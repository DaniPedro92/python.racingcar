import pygame
import configs
import math
import random

class My_car:
    def __init__(self, max_vel, rotation_vel, x, y):
        self.img = configs.img.MY_CAR
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x = x
        self.y = y
        self.acceleration = 0.1
        self.health_max = 100
        self.health = self.health_max
        
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, screen):
        rotate_img = pygame.transform.rotate(self.img, self.angle)
        new_rect = rotate_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotate_img, new_rect.topleft)

    def move_forward(self):
        if self.health <= 75:
            self.max_vel = 3.5
        elif self.health <= 50:
            self.max_vel = 3
        elif self.health <= 25:
            self.max_vel = 2.5
        else:
            self.max_vel = 4
        if self.health <= 0:
            self.max_vel = 0
        
            
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        forward = math.cos(radians) * self.vel
        sideways = math.sin(radians) * self.vel

        self.y -= forward
        self.x -= sideways

    def reduce_vel(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def collide_with(self, mask, mask_offset_x=0, mask_offset_y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (self.x - mask_offset_x, self.y - mask_offset_y)
        overlap_area = mask.overlap_area(car_mask, offset)
        return overlap_area
    
    def rebound(self):
        self.vel = -self.vel
        self.move()

    def take_damage(self, damage_amount):
        self.health -= damage_amount
        if self.health <= 0:
            self.health = 0

    def spin_out(self):
        random_angle = random.randint(-45, 45)
        self.angle += random_angle

    def boost(self):
        self.vel += 8
        self.move()

    