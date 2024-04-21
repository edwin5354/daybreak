import pygame

# Music/ Sound
bg_music = pygame.mixer.Sound("Sound/kapustin.mp3")
bg_music.set_volume(0.45)
bg_music.play(-1)

jump_sound = pygame.mixer.Sound("Sound/jump.mp3")
jump_sound.set_volume(0.65)

portal_sound = pygame.mixer.Sound("Sound/portal.mp3")
portal_sound.set_volume(0.08)

coin_sound = pygame.mixer.Sound("Sound/coin_sound.mp3")
coin_sound.set_volume(0.7)

carrot_sound = pygame.mixer.Sound("Sound/health.wav")
carrot_sound.set_volume(0.6)

screen_sound = pygame.mixer.Sound("Sound/screen.mp3")
screen_sound.set_volume(0.075)

hurt_sound = pygame.mixer.Sound("Sound/hurt.wav")
hurt_sound.set_volume(0.3)

spike_sound = pygame.mixer.Sound("Sound/spike.mp3")
spike_sound.set_volume(0.5)

cactus_sound = pygame.mixer.Sound("Sound/ouch.mp3")
cactus_sound.set_volume(0.65)

grass_broke_sound = pygame.mixer.Sound("Sound/grass_broke.mp3")
grass_broke_sound.set_volume(8)

game_over_sound = pygame.mixer.Sound("Sound/game_over.wav")
game_over_sound.set_volume(0.4)

bubble_sound = pygame.mixer.Sound("Sound/bubble.mp3")
bubble_sound.set_volume(0.8)

jetpack_sound = pygame.mixer.Sound("Sound/jetpack_sound.mp3")
jetpack_sound.set_volume(3)

jetpack_pickup_sound = pygame.mixer.Sound("Sound/jetpack_pick_up.mp3")
jetpack_pickup_sound.set_volume(0.3)

gold_sound = pygame.mixer.Sound("Sound/gold.mp3")
gold_sound.set_volume(0.3)
