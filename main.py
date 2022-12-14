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
pygame.mixer.pre_init(44100, -16, 2, 512)

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
score_font = pygame.font.Font("./fonts/PAC-FONT.ttf", 15)
title_font = pygame.font.Font("./fonts/PAC-FONT.ttf", 80)

running = True
flicker = False

movementDirectionX = 0
movementDirectionY = 0

gateFlag = True

name = ""

menuOption = 0 #0 for start, 1 for quit

timer = myTimer.Timer(0.3)
timer.start_timer()

levelCount = 1

highscores = []

player = player.Player()
player_hitbox = pygame.draw.circle(screen, (0,0,0), (player.x+13, player.y+13), 13)

enemies = [enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/red.png"), (26,26))), enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/blue.png"), (26,26))),
enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/orange.png"), (26,26))), enemy.Enemy(0.8/levelCount, pygame.transform.scale( pygame.image.load("./assets/pink.png"), (26,26)))]

poweredUp = False
player_lives = 3

def genericBlit(x, y, img):
    screen.blit(img, (x,y))

def draw_board():
    global dots_left, poweredUp, score
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
                    score+=10
                    
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

                    for enemy in enemies:
                        if not (enemy.dead) and  not enemy.inSpawn:
                            if not (enemy.powerUpTimer is None):
                                enemy.powerUpTimer.kill_thread()
                            
                            enemy.powerUpTimer = myTimer.Timer(7)
                            enemy.powerUpTimer.start_timer()
                        

                    
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
                                


def load_scores():
    global highscores
    
    with open("./data/data.txt", 'r') as f:
        lines = f.readlines()
        highscores.clear()
        for x in range(len(lines)):
            n = lines[x].strip()
            tup = n.split(":")
            tup = (tup[0], int(tup[1]))
            highscores.append(tup)
            
        
        highscores = sorted(highscores, key=lambda x: x[1], reverse=True)
        
        f.close()




def end_game():
    global level, levelCount, dots_left, player_lives, score
    restart = False

    title1 = title_font.render("GAME OVER", True, (200, 250,0))
    title2 = title_font.render("PRESS ENTER", True, (255,255,255))

    while not restart:
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_RETURN]:
                restart = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((0,0,0))
        screen.blit(title1, (100,300))
        screen.blit(title2, (100, 500))
        pygame.display.update()
        clock.tick(60)

    dots_left = 246
    player_lives = 3
    level = copy.deepcopy(board.boards)
    levelCount = 1
    
    player.restart()

    for enemy in enemies:
        enemy.restart()
    
def high_score_screen():
    global highscores
    running = True

    highscore_title = pygame.font.Font("./fonts/PAC-FONT.ttf", 40)
    regularscore = pygame.font.Font("./fonts/ARCADE_I.ttf", 24)

    screen_index = 1

    title = highscore_title.render("HIGH-SCORES", True, (200,250,0))

    while running:
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()

            if keystate[pygame.K_BACKSPACE]:
                running = False
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        

        screen.fill((0,0,0))
        screen.blit(title, (270,100))
        

        number = 1
        y_coord = 180
        for x in highscores:
            if number >= 10:
                break
            spot = regularscore.render(f"{number}. {x[0]}        {x[1]}", True, (255,255,255))
            screen.blit(spot, (230, y_coord))
            y_coord+=50
            number+=1
            
        
        pygame.display.update()
        clock.tick(60)

def next_level():
    global level, levelCount, dots_left
    proceed = False

    while not proceed:
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_RETURN]:
                proceed = True

            if event.type == pygame.QUIT:
                pygame.quit()
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

        if enemy.powerUpTimer is None and not enemy.dead:
            if (playerX1 < enemyX2 and playerX2 > enemyX1 and playerY1 < enemyY2 and playerY2 > enemyY1):
                collision = True
                break
        else:
            if (playerX1 < enemyX2 and playerX2 > enemyX1 and playerY1 < enemyY2 and playerY2 > enemyY1):
                enemy.swapToDead()
                enemy.dead = True
                enemy.powerUpTimer = None
                
                    
                
            
    
    return collision




def start_game():
    global flicker, movementDirectionY, movementDirectionX, dots_left, player_lives, poweredUp,score, gateFlag
    gameLoop = True
    timer = myTimer.Timer(0.8)
    timer.start_timer()
    level = copy.deepcopy(board.boards)
    score = 0
    
    gateTimer = myTimer.Timer(5)
    gateTimer.start_timer()
    gateFlag = False

    while gameLoop:  
        score_ft = main_font.render(f"SCORE: {score}", False, (255,255,255))
        live_score = main_font.render("Lives: ", True, (255,255,255))
        paclife = score_font.render("c", False, (220,255,0))
        flicker = timer.get_status()

        if gateTimer.get_status():
            gateTimer.kill_thread()
            gateFlag = True

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

        player.handle_movement(movementDirectionX, movementDirectionY)
        player_hitbox.centerx = player.x+13
        player_hitbox.centery = player.y+13


        for x in enemies:
            if not (x.powerUpTimer is None):
                if x.powerUpTimer.get_status() == True:
                    
                    x.powerUpTimer.kill_thread()
                    x.powerUpTimer = None
                    x.swapToNormal()

            x.handleMovement(player)
       

        if checkCollisions(player, enemies, poweredUp):
            player_lives -= 1
            player.restart()

        if player_lives == 0:
            timer.kill_thread()
            end_game()
            break

        
        screen.fill((0,0,0))
        draw_board()

        if poweredUp:
            for x in enemies:
                if not x.dead and not (x.powerUpTimer is None):
                    x.swapToPowerup()
                    
                
                elif not x.deadTimer is None:
                    if x.deadTimer.get_status():
                        x.deadTimer.kill_thread()
                        x.deadTimer = None
                        x.dead = False
                        x.swapToNormal()
        
        genericBlit(player.x, player.y, player.img)
        screen.blit(score_ft, (50,920))
        screen.blit(live_score, (500, 920))

        neX = 650
        neY = 925
        for x in range(player_lives):
            screen.blit(paclife, (neX, neY))
            neX+=30
        
       
        for x in enemies:
            genericBlit(x.x, x.y, x.img)
        
        if dots_left == 0:
            next_level()
            

        pygame.display.update()
        clock.tick(60)


#This will be the main menu of the game

over_font = main_font.render("START", True, (255, 255, 255))
high_score = main_font.render("HIGH-SCORES", True, (255,255,255))
end_font = main_font.render("QUIT", True, (255, 255, 255))
title = title_font.render("pac-man", True, (220,250,0))

while running:
    flicker = timer.get_status()

    for event in pygame.event.get():
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_DOWN]:
            if menuOption < 2:
                menuOption += 1
        elif keystate[pygame.K_UP]:
            if menuOption > 0:
                menuOption -= 1
        elif keystate[pygame.K_RETURN]:
            if menuOption == 0:
                timer.kill_thread()
                create_profile()
                timer = myTimer.Timer(0.3)
                timer.start_timer()
            elif menuOption == 1:
                timer.kill_thread()
                load_scores()
                high_score_screen()
                timer = myTimer.Timer(0.3)
                timer.start_timer()
            else:
                timer.kill_thread()
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            timer.kill_thread()
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    screen.blit(title, (210,150))

    if flicker == False and menuOption == 2:
        screen.blit(over_font, (350,300))
        screen.blit(high_score, (350, 400))
    elif flicker == False and menuOption == 0:
        screen.blit(end_font, (350,500))
        screen.blit(high_score, (350, 400))
    elif flicker == False and menuOption == 1:
        screen.blit(over_font, (350,300))
        screen.blit(end_font, (350,500))
    else:
        screen.blit(over_font, (350,300))
        screen.blit(end_font, (350,500))
        screen.blit(high_score, (350, 400))
   
    pygame.display.update()
    clock.tick(60)




    def create_profile():
        global name

        firstChar = ''
        secondChar = ''
        thirdChar = ''
        index = 0

        title = main_font.render("Enter a name", True, (255,255,255))
        f_und = main_font.render("_", True, (255,255,255))
        enter = main_font.render("Enter to continue", True, (255,255,255))

        b = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_RETURN]:
                        if index == 3:
                            name = name + firstChar + secondChar + thirdChar
                            start_game()
                            with open("./data/data.txt", "a+") as file_object:
                                # Move read cursor to the start of file.
                                file_object.seek(0)
                                
                                data = file_object.read(100)
                                if len(data) > 0 :
                                    file_object.write("\n")
                                
                                file_object.write(name + f":{score}")
                            b = True
                            break
                    elif keystate[pygame.K_BACKSPACE]:
                        if index == 3:
                            thirdChar = ' '
                        elif index == 2:
                            secondChar = ' '
                        elif index == 1:
                            firstChar = ' '
                        if index > 0 :
                            index -=1
                    else:
                        if event.unicode.isalpha():
                            if index == 0:
                                firstChar = event.unicode
                            elif index == 1:
                                secondChar = event.unicode
                            elif index == 2:
                                thirdChar = event.unicode
                            if index < 3:
                                index+=1
                            

                if event.type == pygame.QUIT:
                    timer.kill_thread()
                    pygame.quit()
                    sys.exit()

            if b:
                break

            screen.fill((0,0,0))
            screen.blit(title, (320,200))
            screen.blit(f_und, (400,400))
            screen.blit(f_und, (440,400))
            screen.blit(f_und, (480,400))

            f_ch = main_font.render(firstChar, True, (255,255,255))
            s_ch = main_font.render(secondChar, True, (255,255,255))
            t_ch = main_font.render(thirdChar, True, (255,255,255))

            screen.blit(f_ch, (400, 380))
            screen.blit(s_ch, (440, 380))
            screen.blit(t_ch, (480, 380))

            if index == 3:
                screen.blit(enter, (420, 500))

            pygame.display.update()
            clock.tick(60)
