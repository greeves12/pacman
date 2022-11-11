import pygame

class Player():

    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load("./assets/1.png"), (80,50))
        
        self.x = 370
        self.y = 480
        self.x_change = 0
        self.changeMultiplier = 6
    
    def change_player_img(self,img):
        self.img = pygame.transform.scale(pygame.image.load(img), (80,50))

    def handle_movement(self, movementX, movementY):
        