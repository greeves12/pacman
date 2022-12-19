import pygame
import board
import random
import myTimer
import math

class Enemy():

    doNewTurn = True
    powerUpImage = pygame.transform.scale(pygame.image.load("./assets/powerup.png"), (26,26))
    normalImage = pygame.transform.scale( pygame.image.load("./assets/red.png"), (26,26))
    turns = [False,False,False,False]
    direction = 0
    level = board.boards
    startX = 440 #440
    startY = 440 #340
    dead = False
    deadImg = pygame.transform.scale(pygame.image.load("./assets/dead.png"), (26,26))
    powerUpTimer = None
    deadTimer = None
    oldTurn = 0
    spawnAnimation = False
    inSpawn = True
    list = [-1,1]
    direct = 1
    moveOut = False
    changeMultiplier = 2

    timerToMove = None

    def __init__(self, randomMove, imgage):
        self.x = random.randint(421, 459)
        self.y = self.startY
        self.normalImage = imgage
        self.img = self.normalImage
        self.changeMultiplier = 2
        self.randomMoveChance = randomMove
        self.direct = random.choice(self.list)
        self.timerToMove = myTimer.Timer(5)
       
        

    def reset(self):
        self.x = self.startX
        self.y = self.startY
    def swapToDead(self):
        self.img = self.deadImg

    def restart(self):
        self.x = self.startX
        self.y = self.startY

    def swapToPowerup(self):
        self.img = self.powerUpImage
        
    
    def swapToNormal(self):
        self.img = self.normalImage
    
    def enterSpawnAnimation(self):
        if not (self.y >= 439 and self.y <= 445):
            self.y += 1 * self.changeMultiplier
        else:
            self.spawnAnimation = False
            self.inSpawn = True
            self.timerToMove = myTimer.Timer(5)
            self.timerToMove.start_timer()



    def returnToSpawn(self):
        self.changeMultiplier = 3
        x = 440
        y = 340

        if (self.x >= 439 and self.x <= 442) and (self.y >= 339 and self.y <= 342):
            self.dead = False
            self.swapToNormal()
            self.spawnAnimation = True
            return

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

            if self.direction == 0 or self.direction == 1:       
                if self.turns[self.direction]:
                    
                    if self.turns[2] and self.turns[3]:
                        
                        pythTop = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y-10 - y, 2)))
                        pythBottom = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y+10 - y, 2)))

                        pythCur = 0

                        if self.direction == 0:
                            pythCur = math.sqrt( (math.pow(self.x+10 - x, 2)) + (math.pow(self.y - y, 2)))
                        else:
                            pythCur = math.sqrt( (math.pow(self.x-10 - x, 2)) + (math.pow(self.y - y, 2)))

                        pythMin = min(pythCur, pythTop, pythBottom)


                        if pythTop == pythMin:
                            self.direction = 2
                        elif pythCur == pythMin:
                            self.direction = self.direction
                        else:
                            
                            self.direction = 3

                    elif self.turns[2]:

                        pythTop = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y-10 - y, 2)))
                        pythCur = 0

                        if self.direction == 0:
                            pythCur = math.sqrt( (math.pow(self.x+10 - x, 2)) + (math.pow(self.y - y, 2)))
                        else:
                            pythCur = math.sqrt( (math.pow(self.x-10 - x, 2)) + (math.pow(self.y - y, 2)))


                        if pythCur >= pythTop:
                            self.direction = 2
                        else:
                            self.direction = self.direction  
                    else:
                        pythTop = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y+10 - y, 2)))
                        pythCur = 0

                        if self.direction == 0:
                            pythCur = math.sqrt( (math.pow(self.x+10 - x, 2)) + (math.pow(self.y - y, 2)))
                        else:
                            pythCur = math.sqrt( (math.pow(self.x-10 - x, 2)) + (math.pow(self.y - y, 2)))


                        if pythCur >= pythTop:
                            self.direction = 3
                        else:
                            self.direction = self.direction  
                
                elif self.turns[2] and self.turns[3]:
                    
                    pythTop = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y-10 - y, 2)))
                    pythBottom = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y+10 - y, 2)))

                    if pythTop >= pythBottom:
                        self.direction = 3
                    else:
                        self.direction = 2
                elif self.turns[2]:
                    self.direction = 2
                else:
                    
                    self.direction = 3

            elif self.direction == 2 or self.direction == 3:
                if self.turns[self.direction]:
                    if self.turns[0] and self.turns[1]:
                        pythTop = math.sqrt( (math.pow(self.x+10 - x, 2)) + (math.pow(self.y - y, 2)))
                        pythBottom = math.sqrt( (math.pow(self.x-10 - x, 2)) + (math.pow(self.y - y, 2)))

                        pythCur = 0

                        if self.direction == 2:
                            pythCur = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y-10 - y, 2)))
                        else:
                            pythCur = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y+10 - y, 2)))

                        pythMin = min(pythCur, pythTop, pythBottom)


                        if pythTop == pythMin:
                            self.direction = 0
                        elif pythCur == pythMin:
                            self.direction = self.direction
                        else:
                            self.direction = 1

                    elif self.turns[0]:
                        pythRight = math.sqrt( (math.pow(self.x+10 - x, 2)) + (math.pow(self.y - y, 2)))
                        pythCur = 0

                        if self.direction == 2:
                            pythCur = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y-10 - y, 2)))
                        else:
                            pythCur = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y+10 - y, 2)))
                        
                        if pythCur >= pythRight:
                            self.direction = 0
                        else:
                            self.direction = self.direction

                    else:
                        pythLeft = math.sqrt( (math.pow(self.x-10 - x, 2)) + (math.pow(self.y - y, 2)))
                        pythCur = 0

                        if self.direction == 2:
                            pythCur = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y-10 - y, 2)))
                        else:
                            pythCur = math.sqrt( (math.pow(self.x - x, 2)) + (math.pow(self.y+10 - y, 2)))
                        
                        if pythCur >= pythLeft:
                            self.direction = 1
                        else:
                            self.direction = self.direction

                elif self.turns[0] and self.turns[1]:
                    pythTop = math.sqrt( (math.pow(self.x+10 - x, 2)) + (math.pow(self.y - y, 2)))
                    pythBottom = math.sqrt( (math.pow(self.x-10 - x, 2)) + (math.pow(self.y - y, 2)))

                    if pythTop >= pythBottom:
                        self.direction = 1
                    else:
                        self.direction = 0
                elif self.turns[0]:
                    self.direction = 0
                else:
                    self.direction = 1

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

    
    def moveInSpawn(self):
        if self.timerToMove.get_status():
            self.timerToMove.kill_thread()
            self.moveOut = True
            self.inSpawn = False

        if self.x > 460:
            self.direct *= -1
            
        elif self.x < 420:
            self.direct *= -1

        self.x += self.direct
       
    def moveOutOfSpawn(self):
        if self.x < 440:
            self.x += 1
        elif self.x > 440:
            self.x -= 1
        else:
            if self.y > 339:
                self.y -= 1
            else:
                self.moveOut = False 
        

    def handleMovement(self, player):
        doRandom = False
        

        if self.spawnAnimation:
            self.enterSpawnAnimation()
            return        
        
        if self.dead:
            self.returnToSpawn()
            return
        
        if self.inSpawn:
            self.moveInSpawn()
            self.changeMultiplier = 2
            return

        if self.moveOut:
            self.moveOutOfSpawn()
            return

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
            randomMove = random.randrange(1,100)
      
            if (randomMove <= (self.randomMoveChance*100)) and (randomMove >= 0):
                doRandom = True
            
            if not self.powerUpTimer is None:
                #Run away from the player

                
                rando = random.randint(0,3)
                
                while self.turns[rando] == False :
                    rando = random.randint(0,3)
                    
                self.direction = rando  

            else:      
                
                if self.direction == 0 or self.direction == 1:
                    
                    if self.turns[self.direction]:
                        
                        if self.turns[2] and self.turns[3]:
                            
                            pythTop = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y-10 - player.y, 2)))
                            pythBottom = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y+10 - player.y, 2)))

                            pythCur = 0

                            if self.direction == 0:
                                pythCur = math.sqrt( (math.pow(self.x+10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))
                            else:
                                pythCur = math.sqrt( (math.pow(self.x-10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))

                            pythMin = min(pythCur, pythTop, pythBottom)


                            if pythTop == pythMin:
                                self.direction = 2
                            elif pythCur == pythMin:
                                self.direction = self.direction
                            else:
                                
                                self.direction = 3

                        elif self.turns[2]:

                            pythTop = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y-10 - player.y, 2)))
                            pythCur = 0

                            if self.direction == 0:
                                pythCur = math.sqrt( (math.pow(self.x+10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))
                            else:
                                pythCur = math.sqrt( (math.pow(self.x-10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))


                            if pythCur >= pythTop:
                                self.direction = 2
                            else:
                                self.direction = self.direction  
                        else:
                            pythTop = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y+10 - player.y, 2)))
                            pythCur = 0

                            if self.direction == 0:
                                pythCur = math.sqrt( (math.pow(self.x+10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))
                            else:
                                pythCur = math.sqrt( (math.pow(self.x-10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))


                            if pythCur >= pythTop:
                                self.direction = 3
                            else:
                                self.direction = self.direction  
                    
                    elif self.turns[2] and self.turns[3]:
                        
                        pythTop = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y-10 - player.y, 2)))
                        pythBottom = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y+10 - player.y, 2)))

                        if pythTop >= pythBottom:
                            self.direction = 3
                        else:
                            self.direction = 2
                    elif self.turns[2]:
                        self.direction = 2
                    else:
                        
                        self.direction = 3

                elif self.direction == 2 or self.direction == 3:
                    if self.turns[self.direction]:
                        if self.turns[0] and self.turns[1]:
                            pythTop = math.sqrt( (math.pow(self.x+10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))
                            pythBottom = math.sqrt( (math.pow(self.x-10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))

                            pythCur = 0

                            if self.direction == 2:
                                pythCur = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y-10 - player.y, 2)))
                            else:
                                pythCur = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y+10 - player.y, 2)))

                            pythMin = min(pythCur, pythTop, pythBottom)


                            if pythTop == pythMin:
                                self.direction = 0
                            elif pythCur == pythMin:
                                self.direction = self.direction
                            else:
                                self.direction = 1

                        elif self.turns[0]:
                            pythRight = math.sqrt( (math.pow(self.x+10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))
                            pythCur = 0

                            if self.direction == 2:
                                pythCur = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y-10 - player.y, 2)))
                            else:
                                pythCur = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y+10 - player.y, 2)))
                            
                            if pythCur >= pythRight:
                                self.direction = 0
                            else:
                                self.direction = self.direction

                        else:
                            pythLeft = math.sqrt( (math.pow(self.x-10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))
                            pythCur = 0

                            if self.direction == 2:
                                pythCur = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y-10 - player.y, 2)))
                            else:
                                pythCur = math.sqrt( (math.pow(self.x - player.x, 2)) + (math.pow(self.y+10 - player.y, 2)))
                            
                            if pythCur >= pythLeft:
                                self.direction = 1
                            else:
                                self.direction = self.direction

                    elif self.turns[0] and self.turns[1]:
                        pythTop = math.sqrt( (math.pow(self.x+10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))
                        pythBottom = math.sqrt( (math.pow(self.x-10 - player.x, 2)) + (math.pow(self.y - player.y, 2)))

                        if pythTop >= pythBottom:
                            self.direction = 1
                        else:
                            self.direction = 0
                    elif self.turns[0]:
                        self.direction = 0
                    else:
                        self.direction = 1
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
