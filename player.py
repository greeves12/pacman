import pygame
import board
import math

class Player():
    level = board.boards
    direction = 0
    turns = [False, False, False, False] #right, left, up, down
    animation_counter = 0 #essentially circular list
    player_moving = False
    vetoTime = 10
    vetoDirection = -1
  

    player_images = [pygame.image.load("./assets/1.png"), pygame.image.load("./assets/2.png"), pygame.image.load("./assets/3.png"), pygame.image.load("./assets/4.png")]

    def __init__(self):
        
        self.x = 60
        self.y = 60
        self.x_change = 0
        self.changeMultiplier = 3

        self.img =  pygame.transform.scale(self.player_images[0], (26,26))
    
    def change_player_img(self, direction, img):
        self.img = pygame.transform.scale(img, (26,26))

        if direction == 1:
            self.img = pygame.transform.flip(self.img, True, False)
        elif direction == 2:
            self.img = pygame.transform.rotate(self.img, 90)
        elif direction == 3:
            self.img = pygame.transform.rotate(self.img, 270)

    def handle_movement(self, movementX, movementY):
        self.turns = self.check_position(self.x+13, self.y+13)


        oldDir = self.direction

    
         
        if movementX == 1: #right
            self.direction = 0
        elif movementX == -1: #left
            self.direction = 1
        elif movementY == 1: #down
            self.direction = 3
        elif movementY == -1: #up
            self.direction = 2

        if self.turns[self.direction] == False:
            self.vetoDirection = self.direction
            self.direction = oldDir

           

        if self.vetoDirection != -1 and self.turns[self.vetoDirection]:
            self.direction = self.vetoDirection
            self.vetoDirection = -1
            self.vetoTime = 10

            
        
        if self.vetoTime == 0 and self.vetoDirection != -1:
            self.vetoTime = 10
            self.vetoDirection = -1

        if self.direction == 0:
            movementX = 1
        elif self.direction == 1:
            movementX = -1

        if self.direction == 2:
            movementY = -1
        elif self.direction == 3:
            movementY = 1
    
        
       # print(self.turns)
        self.player_moving = False
        print(self.direction)

        if self.direction == 0 and self.turns[0]:
            self.x += movementX * self.changeMultiplier
            self.player_moving = True
        elif self.direction == 1 and self.turns[1]:
            self.x += movementX * self.changeMultiplier
            self.player_moving = True

        if self.direction == 2 and self.turns[2]:
            self.y += movementY * self.changeMultiplier
            self.player_moving = True
        elif self.direction == 3 and self.turns[3]:
            self.y += movementY * self.changeMultiplier
            self.player_moving = True

        if self.x < 20:
            self.x = 820
        elif self.x > 820:
            self.x = 20


        if movementX == 0 and movementY == 0:
            self.player_moving = False

        if self.player_moving:
            self.change_player_img(self.direction, self.player_images[(self.animation_counter % 4)])
            self.animation_counter += 1
        else:
            self.change_player_img(self.direction, self.player_images[0])
            self.animation_counter = 1


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
