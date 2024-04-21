import pygame

# Basic setup
pygame.init()
clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Daybreak")

# Drawing Background
background_img = pygame.image.load('PNG/Background/bg_layer.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (450, 700))

# Game Variables
scroll = 0
SCROLL_THRESH = 250
MAX_PLATFORMS = 6
MAX_ENEMIES = 4

title_bunny = pygame.image.load("PNG/Players/idle/0.png").convert_alpha()
bubble_bunny = pygame.image.load("PNG/Powerups/bubble_player.png").convert_alpha()
bubble_bunny = pygame.transform.scale(bubble_bunny, (int(bubble_bunny.get_width() * 0.3), int(bubble_bunny.get_height() * 0.3)))

# HUD / collectibles
life_img = pygame.image.load("PNG/HUD/lifes.png").convert_alpha()
life_img = pygame.transform.scale(life_img, (int(life_img.get_width() * 0.6), int(life_img.get_height() * 0.6)))

coin_img = pygame.image.load("PNG/HUD/coin_gold.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (int(coin_img.get_width() * 0.6), int(coin_img.get_height() * 0.6)))
