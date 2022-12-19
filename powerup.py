import pygame
import random
import board

class Powerup():
    level = board.boards
    direction = 0
    turns = [False, False, False, False] #right, left, up, down
    animation_counter = 0 #essentially circular list
    player_moving = False
    vetoTime = 5
    vetoDirection = -1
    startX = 440
    startY = 505
    doNewTurn = True

    player_images = [pygame.image.load("./assets/powerup-box.jpg")]

    def __init__(self):
        
        self.x = self.startX
        self.y = self.startY
        self.x_change = 0
        self.changeMultiplier = 1

        self.img =  pygame.transform.scale(self.player_images[0], (26,26))

    def restart(self):
        self.x = self.startX
        self.y = self.startY
       

    def handleMovement(self):
       
        self.changeMultiplier = 2

        nextTurn = self.check_position(self.x+13, self.y+13)

        if not self.doNewTurn:
            if self.direction == 0 or self.direction == 1:
                if nextTurn[3] or nextTurn[2]:
                    if nextTurn != self.oldTurn:
                        self.doNewTurn = True
            elif self.direction == 2 or self.direction == 3:
                if nextTurn[0] or nextTurn[1]:
                    if nextTurn != self.oldTurn:
                        self.doNewTurn = True

        if self.doNewTurn:
            self.doNewTurn = False
            self.oldTurn = nextTurn
            self.turns = nextTurn
           
            rando = random.randint(0,3)
                
            while self.turns[rando] == False :
                rando = random.randint(0,3)
                    
            self.direction = rando 


        if self.direction == 0 and self.turns[0]:
            self.x += 1 * self.changeMultiplier
       
        elif self.direction == 1 and self.turns[1]:
            self.x += -1 * self.changeMultiplier
                

        if self.direction == 2 and self.turns[2]:
            self.y += -1 * self.changeMultiplier
                
        elif self.direction == 3 and self.turns[3]:
            self.y += 1 * self.changeMultiplier
            
           

        if self.x < 20:
           self.x = 820
        elif self.x > 820:
            self.x = 20 
    

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