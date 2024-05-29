import pygame
import configs
from car import My_car
import math

class CPU_car(My_car):
    def __init__(self, max_vel, rotation_vel, x, y, path=[]):
        super().__init__(max_vel, rotation_vel, x, y)
        self.path = path
        self.img = configs.img.CPU_CAR
        self.current_point = 0
        self.target_radius = 5     

    def move(self):
        if self.current_point >= len(self.path):
            return

        target_x, target_y = self.path[self.current_point]
        distance_to_target = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        if distance_to_target <= self.target_radius:
            self.current_point += 1
            if self.current_point >= len(self.path):
                self.current_point = 0
                return 

        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        target_angle_deg = math.degrees(desired_radian_angle)

        self.angle = round(target_angle_deg / 45) * 45

        radians = math.radians(self.angle)
        forward = math.cos(radians) * self.max_vel
        sideways = math.sin(radians) * self.max_vel

        self.y -= forward
        self.x -= sideways

    def rotate(self, left=False, right=False):
        pass

