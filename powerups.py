import pygame
from settings import *

class Powerup(pygame.sprite.Sprite):
    def __init__(self,x,y, type):
        super().__init__()
        self.type = type
        self.image = pygame.image.load(f'PNG/Powerups/{self.type}.png').convert_alpha()  
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def show_portal(self):
        if self.type == 'portal_orange':
            screen.blit(self.image, (self.rect.x, self.rect.y))
  
    def update(self):
        self.show_portal()
