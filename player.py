import pygame
import board
import math

class Player():
    level = board.boards
    direction = 0
    turns = [False, False, False, False]
    animation_counter = 0 #essentially circular list

    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load("./assets/1.png"), (50,50))
        
        self.x = 60
        self.y = 60
        self.x_change = 0
        self.changeMultiplier = 4
    
    def change_player_img(self,img):
        self.img = pygame.transform.scale(pygame.image.load(img), (26,26))

    def handle_movement(self, movementX, movementY):
        if movementX == 1:
            self.direction = 0
        elif movementX == -1:
            self.direction = 1
        elif movementY == 1:
            self.direction = 3
        elif movementY == -1:
            self.direction = 2
        
        self.turns = self.check_position(self.x+13, self.y+13)
        print(self.turns)


        if self.direction == 0 and self.turns[0]:
            self.x += movementX * self.changeMultiplier
        elif self.direction == 1 and self.turns[1]:
            self.x += movementX * self.changeMultiplier
        if self.direction == 2 and self.turns[2]:
            self.y += movementY * self.changeMultiplier
        elif self.direction == 3 and self.turns[3]:
            self.y += movementY * self.changeMultiplier


    def check_position(self, centerx, centery):
        turns = [False, False, False, False]
        num1 = (950 - 50) // 32
        num2 = (900 // 30)
        num3 = 15
        # check collisions based on center x and center y of player +/- fudge number
        if centerx // 30 < 29:
            if self.direction == 0:
                if self.level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
            if self.direction == 1:
                if self.level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
            if self.direction == 2:
                if self.level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
            if self.direction == 3:
                if self.level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= centerx % num2 <= 18:
                    if self.level[(centery + num3) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if self.level[(centery - num3) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if self.level[centery // num1][(centerx - num2) // num2] < 3:
                        turns[1] = True
                    if self.level[centery // num1][(centerx + num2) // num2] < 3:
                        turns[0] = True
            if self.direction == 0 or self.direction == 1:
                if 12 <= centerx % num2 <= 18:
                    if self.level[(centery + num1) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if self.level[(centery - num1) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if self.level[centery // num1][(centerx - num3) // num2] < 3:
                        turns[1] = True
                    if self.level[centery // num1][(centerx + num3) // num2] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns
