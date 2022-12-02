import pygame
import player
import board
import myTimer
import sys
import math
import time
import enemy
import copy

pygame.init()

clock = pygame.time.Clock()

height = 950
width = 900
PI = math.pi

eating_dot_sound = pygame.mixer.Sound("./media/pacman_chomp.wav")

loaded_eating_sounds = []

screen = pygame.display.set_mode((900, 1000))
pygame.display.set_caption("Pac-Man")

level = copy.deepcopy(board.boards)
score = 0
dots_left = 246

main_font = pygame.font.Font("./fonts/ARCADE_I.ttf", 24)

running = True
flicker = False

movementDirectionX = 0
movementDirectionY = 0

menuOption = 0 #0 for start, 1 for quit

timer = myTimer.Timer(0.3)
timer.start_timer()

levelCount = 5

player = player.Player()
player_hitbox = pygame.draw.circle(screen, (0,0,0), (player.x+13, player.y+13), 13)

enemies = [enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/red.png"), (26,26))), enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/blue.png"), (26,26))),
enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/orange.png"), (26,26))), enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/pink.png"), (26,26)))]

poweredUp = False
player_lives = 3

def genericBlit(x, y, img):
    screen.blit(img, (x,y))

def draw_board():
    global dots_left, poweredUp
    color = (0, 0, 255)
    num1 = ((height - 50) // 32) # This is because there are 32 tiles in each columnn
    num2 = (width // 30) # This is because there are 30 tiles in each row

    for i in range(len(level)):
        for j in range(len(level[i])):
            x = j * num2 + (0.5 * num2)
            y = i * num1 + (0.5 * num1)
            point_calculator = math.sqrt((math.pow((player_hitbox.centerx - x), 2) + (math.pow((player_hitbox.centery - y), 2))))
            

            if level[i][j] == 1:
                if point_calculator < (4 + 13):
                    level[i][j] = 0
                    loaded_eating_sounds.append((math.floor(x), math.floor(y)))
                    dots_left -= 1
                else:
                    pygame.draw.circle(screen, 'white', (x, y), 4)
            if level[i][j] == 2:
                if point_calculator < (10 + 13):
                    level[i][j] = 0
                    dots_left -=1
                    screen.fill((0,0,0))
                    draw_board()
                    genericBlit(player.x, player.y, player.img)
                    pygame.display.update()
                    time.sleep(1)
                    poweredUp = True
                    
                elif not flicker:
                    pygame.draw.circle(screen, 'white', (x, y), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)



def end_game():
    global level, levelCount, dots_left, player_lives
    restart = False

    while not restart:
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_RETURN]:
                restart = True

            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
        
        screen.fill((0,0,0))
        pygame.display.update()
        clock.tick(60)

    dots_left = 246
    player_lives = 3
    level = copy.deepcopy(board.boards)
    levelCount = 1
    player.restart()

    for enemy in enemies:
        enemy.restart()
    
def next_level():
    global level, levelCount, dots_left
    proceed = False

    while not proceed:
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_RETURN]:
                proceed = True

            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
        screen.fill((0,0,0))
        pygame.display.update()
        clock.tick(60)
    
    level = copy.deepcopy(board.boards)
    levelCount +=1 
    dots_left = 246
    
    player.restart()

    for enemy in enemies:
        enemy.restart()

def checkCollisions(player, enemies, poweredUp):
    collision = False
    playerX1 = player.x
    playerX2 = player.x + 26
    playerY1 = player.y
    playerY2 = player.y + 26


    for enemy in enemies:
        enemyX1 = enemy.x
        enemyX2 = enemy.x+26
        enemyY1 = enemy.y
        enemyY2 = enemy.y + 26

        if not poweredUp:
            if (playerX1 < enemyX2 and playerX2 > enemyX1 and playerY1 < enemyY2 and playerY2 > enemyY1):
                collision = True
                break
        else:
            if (playerX1 < enemyX2 and playerX2 > enemyX1 and playerY1 < enemyY2 and playerY2 > enemyY1):
                enemy.swapToDead()
                enemy.dead = True
                
            
    
    return collision

def start_game():
    global flicker, movementDirectionY, movementDirectionX, dots_left, player_lives
    gameLoop = True
    timer = myTimer.Timer(0.8)
    timer.start_timer()
    level = copy.deepcopy(board.boards)

    while gameLoop:  
         
        flicker = timer.get_status()


        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()

            if keystate[pygame.K_DOWN]:
                movementDirectionX = 0
                movementDirectionY = 1
                
            elif keystate[pygame.K_UP]:
                movementDirectionX = 0
                movementDirectionY = -1
              
            elif keystate[pygame.K_LEFT]:
                movementDirectionY = 0
                movementDirectionX = -1
                
            elif keystate[pygame.K_RIGHT]:
                movementDirectionX = 1
                movementDirectionY = 0
                
            if event.type == pygame.QUIT:
                timer.kill_thread()
                pygame.quit()
                sys.exit()

        gameOver = True
        for x in range(len(level)):
            for y in range(len(level[x])):
                if level[x][y] == 1 or level[x][y] == 2:
                    gameOver = False

        player.handle_movement(movementDirectionX, movementDirectionY)
        player_hitbox.centerx = player.x+13
        player_hitbox.centery = player.y+13


        for x in enemies:
            x.handleMovement(poweredUp, player)
       

        if checkCollisions(player, enemies, poweredUp):
            player_lives -= 1
            player.restart()

        if player_lives == 0:
            end_game()
            break

        
        screen.fill((0,0,0))
        draw_board()

        if poweredUp:
            for x in enemies:
                if not x.dead:
                    x.swapToPowerup()
        
        genericBlit(player.x, player.y, player.img)
       
        for x in enemies:
            genericBlit(x.x, x.y, x.img)
        
        if dots_left == 0:
            next_level()
            

        pygame.display.update()
        clock.tick(60)


#This will be the main menu of the game

over_font = main_font.render("START", True, (255, 255, 255))
end_font = main_font.render("QUIT", True, (255, 255, 255))

while running:
    flicker = timer.get_status()

    for event in pygame.event.get():
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_DOWN]:
            if menuOption == 0:
                menuOption = 1
        elif keystate[pygame.K_UP]:
            if menuOption == 1:
                menuOption = 0
        elif keystate[pygame.K_RETURN]:
            if menuOption == 0:
                timer.kill_thread()
                start_game()
                timer = myTimer.Timer(0.8)
            else:
                timer.kill_thread()
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            timer.kill_thread()
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))

    if flicker == False and menuOption == 1:
        screen.blit(over_font, (320,300))
    elif flicker == False and menuOption == 0:
        screen.blit(end_font, (320,400))
    else:
        screen.blit(over_font, (320,300))
        screen.blit(end_font, (320,400))
   
    pygame.display.update()
    clock.tick(60)