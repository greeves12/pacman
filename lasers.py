import pygame
import math
import random

class Laser():
    def __init__(self):
        self.img = pygame.transform.scale((pygame.image.load("./assets/bullet4.png")), (40,40))
        self.img = pygame.transform.rotate(self.img, 270)
        self.x = (random.randint(2, 735))
        self.y = (random.randint(-100, -40))
        self.x_change = (random.randint(-3,3))

    def mainGameMovement(self):          
        self.x -= self.x_change
        
        if self.x < -25:
            self.x = (random.randint(1000, 1100))
            self.y = (random.randint(150, 800))
            self.x_change = (random.randint(1,5))
            