import pygame
import player
import board
import myTimer
import sys
import math

pygame.init()

clock = pygame.time.Clock()

height = 950
width = 900
PI = math.pi

screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("Pac-Man")

level = board.boards
dots = [[None]*30]*32
score = 0
dots_left = 244

main_font = pygame.font.Font("./fonts/ARCADE_I.ttf", 24)

running = True
flicker = False

movementDirectionX = 0
movementDirectionY = 0

menuOption = 0 #0 for start, 1 for quit

timer = myTimer.Timer(0.3)
timer.start_timer()

player = player.Player()
player_hitbox = pygame.draw.circle(screen, (0,0,0), (player.x, player.y), 13)

def genericBlit(x, y, img):
    screen.blit(img, (x,y))

def draw_board():
    color = (0, 0, 255)
    num1 = ((height - 50) // 32) # This is because there are 32 tiles in each columnn
    num2 = (width // 30) # This is because there are 30 tiles in each row

    for i in range(len(level)):
        for j in range(len(level[i])):
            x = j * num2 + (0.5 * num2)
            y = i * num1 + (0.5 * num1)
            point_calculator = math.sqrt((math.pow((player.x - x), 2) + (math.pow((player.y - y), 2))))

            if level[i][j] == 1:
                if point_calculator < (4 + 13):
                    level[i][j] = 0
                else:
                    pygame.draw.circle(screen, 'white', (x, y), 4)
            if level[i][j] == 2 and not flicker:
                if point_calculator < (4 + 13):
                    level[i][j] = 0
                else:
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
    screen.fill((0,0,0))

def start_game():
    global flicker, movementDirectionY, movementDirectionX
    gameLoop = True
    timer = myTimer.Timer(0.8)
    timer.start_timer()
    gameOver = False
    player_lives = 3

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

        if player_lives == 0:
            gameOver = True
            break

        gameOver = True
        for x in range(len(level)):
            for y in range(len(level[x])):
                if level[x][y] == 1 or level[x][y] == 2:
                    gameOver = False

        if gameOver:
            end_game()


        player.handle_movement(movementDirectionX, movementDirectionY)
        player_hitbox.centerx = player.x
        player_hitbox.centery = player.y

        screen.fill((0,0,0))
        draw_board()
        
        genericBlit(player.x, player.y, player.img)

        

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
                timer = myTimer.Timer()
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