import pygame
import board
import random

class Enemy():

    powerUpImage = pygame.transform.scale(pygame.image.load("./assets/powerup.png"), (26,26))
    normalImage = pygame.transform.scale( pygame.image.load("./assets/red.png"), (26,26))
    turns = [False,False,False,False]
    direction = 0
    level = board.boards
   

    def __init__(self, randomMove):
        self.x = 380
        self.y = 255
        self.img = self.normalImage
        self.changeMultiplier = 3
        self.randomMoveChance = randomMove

    def swapToPowerup(self):
        self.img = self.powerUpImage
    
    def swapToNormal(self):
        self.img = self.normalImage
    
    def handleMovement(self, powerUp, player):
        doRandom = False

        newTurns = self.turns
        if self.direction == 0:
            self.turns[0] = True
        elif self.direction == 1:
            self.turns[1] = True
        elif self.direction == 2:
            self.turns[2] = True
        elif self.direction == 3:
            self.turns[3] = True
        
        nextTurn = self.check_position(self.x+13, self.y+13)

        if nextTurn != newTurns:
            self.turns = nextTurn
            randomMove = random.randrange(1,100)
      
            if (randomMove <= (self.randomMoveChance*100)) and (randomMove >= 0):
                doRandom = True

            equal = player.x - self.x

            if equal < 0:
                equal = equal * -1

            if powerUp:
                #Run away from the player
                False
            else:
            
                if equal < 3:
                    if player.y > self.y:
                        if self.turns[3]:
                            self.direction = 3
                        elif self.turns[0]:
                            self.direction = 0
                    else:
                        if self.turns[2]:
                            self.direction = 2
                        elif self.turns[1]:
                            self.direction =1
                #Chase the player
                elif player.x > self.x:
                    if self.turns[0]: #attempt to move enemy right
                        self.direction = 0
                    elif player.y > self.y:
                        if self.turns[3]:
                            self.direction = 3
                    else:
                        if self.turns[2]:
                            self.direction = 2
                
                elif player.x <= self.x:
                    
                    if self.turns[1]: #attempt to move enemy left                
                        self.direction = 1 
                    elif player.y > self.y:
                        
                        if self.turns[3]:
                            self.direction = 3

                    else:
                        if self.turns[2]:
                            self.direction = 2   


                if doRandom:
                    rando = random.randint(0,3)
                    while self.turns[rando] == False:
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
