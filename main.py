import pygame, sys
from pygame.locals import *
import random
from random import randint, choice
from math import sin
from settings import *
from sounds import *
from powerups import Powerup

# Text
def draw_text(text,x,y,size):
    font = pygame.font.Font('Python/pygame/daybreak/PNG/Font/joystix.ttf', size)
    image = font.render(text, True, 'black')
    screen.blit(image, (x,y))

# Deal with animation type LATER
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.animation_list = []
        self.vel_y = 0
        self.move_animation = ['idle', 'jump', 'hurt']
        self.move_index = 0
        self.move_type = self.move_animation[self.move_index]

        if self.move_type == 'idle': self.num_of_frames = 2
        else: self.num_of_frames = 1

        # Sprite animation --- Bugs unresolved
        for i in range(self.num_of_frames):
            self.animation_list.append(pygame.image.load(f'Python/pygame/daybreak/PNG/Players/{self.move_type}/{i}.png').convert_alpha())
        self.current_frame = 0
        self.image = self.animation_list[int(self.current_frame)]
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.41), int(self.image.get_height() * 0.41)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # animation time
        self.jump = False
        self.health = 3
        self.score = 0
        self.coin = 0

        # portal
        self.num_portal = 0
        self.max_portal = 1

        # invincibility
        self.invincible = False

        # hurt
        self.hurt_time = 0
        self.hit = False

        # jetpack powerup
        self.hit_jetpack = False

        # bubble powerup
        self.hit_bubble = False

    def animation(self):
        # Update animation
        self.current_frame += 0.1 # Speed
        if int(self.current_frame) >= len(self.animation_list):
            self.current_frame = 0
            self.current_frame += 0.1
        self.image = self.animation_list[int(self.current_frame)]
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.41), int(self.image.get_height() * 0.41)))
            
    def movement(self):
        dx = 0
        dy = 0 
        scroll = 0

        # Key presses
        key = pygame.key.get_pressed()

        # Horizontal movement
        if key[pygame.K_LEFT]:
                    dx = -12
        if key[pygame.K_RIGHT]:
                    dx = 12

        # Jump
        if key[pygame.K_SPACE]:
            self.jump = True                
        else:
            self.jump = False

        # Add gravity
        self.vel_y += 1
        dy += self.vel_y   
          
        # Jumping animation
        if self.vel_y < 0:
            self.image = pygame.image.load(f'Python/pygame/daybreak/PNG/Players/jump/0.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.41), int(self.image.get_height() * 0.41)))
        
        # Jetpack jump
        if self.hit_jetpack:
            self.jetpack_powerup()

        if self.vel_y >= 0:
            self.move_index = 0

        if self.vel_y >= 10:
            self.vel_y = 10

        # Set horizontal boundaries:
        if self.rect.left + dx <= 0: 
             dx = -self.rect.left # self.rect.left - self.rect.left = 0
        if self.rect.right + dx >= SCREEN_WIDTH:
             dx = SCREEN_WIDTH - self.rect.right # self.rect.right - self.rect.right = 0 

        # Animation of portal        
        for portal in powerup_group:
            if portal.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height) and self.health > 0:
                if self.rect.bottom < portal.rect.centery and self.vel_y > 0:
                    self.rect.bottom = portal.rect.top
                    dx = 0
                    # Jump animation
                    if self.jump:
                        portal_sound.play()
                        self.jump = False            
                        dy = 0
                        self.vel_y -= 32 
                        portal.kill()    
                        self.num_portal -= 1

        # collision to platform
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height) and self.health > 0:
                if self.rect.bottom < platform.rect.centery and self.vel_y > 0:
                    self.rect.bottom = platform.rect.top

                    # Moving platforms collision
                    if platform.move_x:
                        dx = platform.direction * platform.speed_x
                    else:
                        dx = 0 # Idle not move          

                    # Jump animation
                    if self.jump:
                        jump_sound.play()
                        self.jump = False            
                        dy = 0
                        self.vel_y -= 32     
                        self.move_index = 1
                        # Jetpack function
                        if self.hit_jetpack:
                            self.vel_y -= 30
                            jetpack_sound.play()
                            self.hit_jetpack = False

                        # Traps for broken platforms
                        if platform.platform_type == 'ground_grass_broken' or platform.platform_type == 'ground_grass_small_broken':
                            grass_broke_sound.play()
                            platform.kill()
                            self.score += 10

		# Scrolling to the top of screen
        if self.rect.top <= SCROLL_THRESH:
		#if player is jumping
            if self.vel_y < 0:
                scroll = -dy

		# update player position
        self.rect.x += dx
        self.rect.y += dy + scroll
        
        return scroll      

    def show_character(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))    
        self.animation()     

    def collision(self):
        if pygame.sprite.spritecollide(player, enemy_group, False) and not self.invincible:
            self.health -= 1
            self.hit = True
            if self.health > 0:
                hurt_sound.play()

        if self.health <= 0:
            self.health = 0
            self.image = pygame.image.load(f'Python/pygame/daybreak/PNG/Players/hurt/0.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.41), int(self.image.get_height() * 0.41)))
    
    def hurt(self):
        if not self.hit_bubble:
            self.duration = 1500
        else:
            self.duration = 5000
            screen.blit(bubble_bunny, (5, 160))
            draw_text('Active', 3, 230, 15)

        if not self.hit:
            self.hurt_time = pygame.time.get_ticks()
            self.image.set_alpha(255)
            
        elif self.hit:
            self.invincible = True
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.duration:
                self.hit = False
                self.invincible = False       
                self.hit_bubble = False
             
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0        

    def jetpack_powerup(self):
        if self.hit_jetpack:
            self.image = pygame.image.load('Python/pygame/daybreak/PNG/Powerups/jetpack_player.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.41), int(self.image.get_height() * 0.41)))
            if self.hit:
                self.hurt()

    def update(self):
        self.show_character()
        self.collision()
        self.hurt()
        self.jetpack_powerup()


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y, char_type, action):
        super().__init__()
        self.animation_list = []
        self.char_type = char_type
        self.action = action

        # Check number of frames for each character:
        if self.char_type == 'flyman': self.num_of_frames = 4
        elif self.char_type == 'wingman': self.num_of_frames = 8
        else: self.num_of_frames = 2

        # Sprite animation
        for i in range(self.num_of_frames):
            self.animation_list.append(pygame.image.load(f'Python/pygame/daybreak/PNG/Enemies/{self.char_type}/{i}.png').convert_alpha())
        self.current_frame = 0
        self.image = self.animation_list[int(self.current_frame)]
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5),
                                                    int(self.image.get_height() * 0.5)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.spawn_time = random.randint(300,600)
        self.direction = random.randint(-1,1)
        self.speed = random.randint(3,5)

    def animation(self):
        # Update animation
        self.current_frame += 0.1 # Speed
        if int(self.current_frame) >= len(self.animation_list):
            self.current_frame = 0
            self.current_frame += 0.1
        self.image = self.animation_list[int(self.current_frame)]
        if self.char_type != 'sun':
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))

    def movement(self):
        dx = 0
        dy = 0

        if self.action:  
            if self.char_type == 'wingman' or self.char_type == 'flyman':
                dx += self.speed * self.direction
            
            if self.char_type == 'spikeball' or self.char_type == 'cloud':
                self.direction = 0
            
            if self.char_type == 'spikeball':
                dy += random.randint(8,10)

            # Update position
            self.rect.x += dx
            self.rect.y += dy
           
    def destroy(self):
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if self.char_type == 'flyman' and self.rect.right < 0:
            self.kill()
        elif self.char_type == 'wingman' and self.rect.left > SCREEN_WIDTH:
            self.kill()
        elif self.char_type == 'spikeball' and self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def update(self):       
        self.movement()
        self.show_character()
        self.destroy()
        if self.char_type != 'sun':
            self.rect.y += scroll

    def show_character(self):
        screen.blit(self.image, (self.rect.x, self.rect.y)) 
        self.animation()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_type, move_x):
        super().__init__()
        self.platform_type = platform_type
        self.img = pygame.image.load(f'Python/pygame/daybreak/PNG/Environment/{self.platform_type}.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * 0.35),
                                                        int(self.img.get_height() * 0.35)))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.move_x = move_x
        self.speed_x = random.randint(1,6)
        self.direction = random.choice([-1,1])

    def draw_platform(self):
        screen.blit(self.img, (self.rect.x,self.rect.y))

    def remove_platform(self):
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            player.score += 10
    
    def moving(self):
        # Horizontal direction
        if self.move_x:
            self.rect.x += self.direction * self.speed_x
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.direction *= -1

    def update(self, scroll):
        self.draw_platform()
        self.moving()
        self.remove_platform()
		#update platform's vertical position
        self.rect.y += scroll


class Decorations(pygame.sprite.Sprite):
    def __init__(self,x,y, dec_type, show):
        super().__init__()
        self.dec_type = dec_type
        self.image = pygame.image.load(f'Python/pygame/daybreak/PNG/Static/{self.dec_type}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.4),
                                                        int(self.image.get_height() * 0.4)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.show = show
    
    def update(self, scroll):
        if self.show:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.rect.y += scroll
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

        if pygame.sprite.spritecollide(self, player_single, False) and self.show:
            if self.dec_type == 'cactus' or self.dec_type == 'spike_top' or self.dec_type == 'spikes_top':
                if not player.invincible:
                    player.health -= 1
                    player.hit = True
                    self.kill()
                    if self.dec_type != 'cactus':
                        spike_sound.play()
                    else:
                        cactus_sound.play()

            if self.dec_type == 'coin':
                coin_sound.play()
                self.kill()
                player.score += 20
                player.coin += 1
            if self.dec_type == 'carrot' and player.health < 7:
                carrot_sound.play()
                self.kill()
                player.health += 1
                if player.health >=7: player.health = 7
            if self.dec_type == 'carrot_gold' and player.health < 7:
                gold_sound.play()
                self.kill()
                player.health += 3
                if player.health >=7: player.health = 7
            if self.dec_type == 'powerup_jetpack':
                jetpack_pickup_sound.play()
                self.kill()
                player.hit_jetpack = True
                player.jetpack_powerup()
            if self.dec_type == 'powerup_bunny' and player.num_portal == 0:
                portal_sound.play()
                self.kill()
                player.num_portal += 1
                portal = Powerup(random.randint(120, SCREEN_WIDTH - 120), SCREEN_HEIGHT - random.randint(60,80), 'portal_orange')
                powerup_group.add(portal)   
            if self.dec_type == 'powerup_bubble' and not player.hit_bubble:
                bubble_sound.play()
                self.kill()
                player.hit = True
                player.hit_bubble = True
                player.hurt()

# Create sprite groups
player_single = pygame.sprite.GroupSingle()
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# Instances for sprites
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)  
player_single.add(player)

# Starting position
start_pos = Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 'ground_grass', False)
platform_group.add(start_pos)

# Testing enemy movement
sun_img = Enemy(SCREEN_WIDTH - 125, 55, 'sun', False)
enemy_group.add(sun_img)

# Enemy timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, random.randint(4000, 10000))

# Main Game Loop
run = True

# Game State
game_start = False
game_over = False
stage = 1

while run:
    # Start screen
    if not game_start:
        screen.blit(background_img, (0,0)) # Draw background  
        draw_text('Daybreak', 5, 80, 65)
        draw_text("Press S to start!", 5, 485, 31)
        draw_text("A Game of pure luck,", 43, 580, 22)
        draw_text('No skills invovled.', 50, 630, 22)
        screen.blit(title_bunny, (170, 230))

        key = pygame.key.get_pressed()
        if key[pygame.K_s]:   # Press S to start the game    
            game_start = True
            screen_sound.play()
    
    else:
        if not game_over:
            scroll = player.movement()

            # Increased difficulty
            if player.score < 80:  # Bugs not fixed; some issues encountered.
                stage = 1
            elif 80 < player.score < 170:
                stage = 2
            elif 170 < player.score < 300:
                stage = 3
            elif 300 < player.score < 470:
                stage = 4
            elif 470 < player.score < 650:
                stage = 5
            elif 650 < player.score < 900:
                stage = 6
            elif 900 < player.score < 1300:
                stage = 7
            else:
                stage = 8

            screen.blit(background_img, (0,0)) # Draw background  
            
            for platform in platform_group:
                platform.update(scroll)
            
            for decoration in decoration_group:
                decoration.update(scroll)

            for enemy in enemy_group:
                enemy.update()

            # Spawn unlimited platforms
            if len(platform_group) <= MAX_PLATFORMS:
                each_platform_xpos = random.randint(80, SCREEN_WIDTH - 80)
                each_platform_ypos = platform.rect.y - random.randint(85, 180)  

                # Stage difficulty including platforms 
                if stage == 1:
                    platform = Platform(each_platform_xpos, each_platform_ypos, 'ground_grass', False)
                elif stage == 2:
                    platform = Platform(each_platform_xpos, each_platform_ypos, random.choice(['ground_grass', 'ground_grass_small']), False)
                elif stage == 3:
                    platform = Platform(each_platform_xpos, each_platform_ypos, 
                                    random.choice(['ground_grass', 'ground_grass_small', 'ground_grass_broken']), False)    
                elif stage == 4:
                    platform = Platform(each_platform_xpos, each_platform_ypos, 
                                    random.choice(['ground_grass', 'ground_grass_small', 'ground_grass_broken', 'ground_grass_small_broken']), False)    
                elif stage == 5:
                    platform = Platform(each_platform_xpos, each_platform_ypos, 
                                    random.choice(['ground_grass', 'ground_grass_small']), random.choice([True, False, False]))                                  
                elif stage == 6:
                    platform = Platform(each_platform_xpos, each_platform_ypos, 
                                    random.choice(['ground_grass', 'ground_grass_small', 'ground_grass_broken', 'ground_grass_small_broken']), 
                                    random.choice([True,False]))
                elif stage == 7:
                    platform = Platform(each_platform_xpos, each_platform_ypos, 
                                    random.choice(['ground_grass', 'ground_grass_small', 'ground_grass_broken', 'ground_grass_small_broken']), 
                                    random.choice([True, True, False]))
                else:
                    platform = Platform(each_platform_xpos, each_platform_ypos, 
                                    random.choice(['ground_grass', 'ground_grass_broken', 'ground_grass_small_broken']), random.choice([True, True, False]))        
                                                  
                platform_group.add(platform)

                # Decorations + Traps
                if platform.platform_type == 'ground_grass' or  platform.platform_type == 'ground_grass_small':
                    if not platform.move_x:
                        if int(stage) < 3:
                            decoration = Decorations(random.randint(each_platform_xpos - 30, each_platform_xpos + 30),
                                                each_platform_ypos - 30, random.choice(['grass', 'grass_brown', 'coin', 'carrot', 'powerup_jetpack']),
                                                random.choice([True, False, False]))   
                        elif 3 <= int(stage) < 5:                    
                            decoration = Decorations(random.randint(each_platform_xpos - 30, each_platform_xpos + 30),
                                                each_platform_ypos - 30, 
                                                random.choice(['spike_top', 'grass', 'grass_brown', 'coin', 'carrot_gold', 'carrot', 'powerup_bunny', 'powerup_jetpack']), 
                                                random.choice([True, False]))    
                        elif 5 <= int(stage) < 8:
                            decoration = Decorations(random.randint(each_platform_xpos - 30, each_platform_xpos + 30),
                                                each_platform_ypos - 30, 
                                                random.choice(['spike_top', 'grass', 'grass_brown', 'cactus', 'carrot', 'powerup_bunny', 'coin', 'powerup_bubble']), 
                                                random.choice([True, True, False]))                                 
                        else:
                            decoration = Decorations(random.randint(each_platform_xpos - 30, each_platform_xpos + 30),
                                                each_platform_ypos - 30, random.choice(['spike_top', 'grass', 'grass_brown', 'cactus',
                                                                                        'spikes_top', 'powerup_bunny', 'powerup_jetpack', 'carrot', 'powerup_bubble']), 
                                                random.choice([True, False]))                                              

                    decoration_group.add(decoration)

            # Enemies
            if len(enemy_group) <= MAX_ENEMIES:
                for enemy in enemy_group:
                    x_pos = -100 # Initial x_pos
                    y_pos = player.rect.top - randint(80,150)
                    if enemy.direction == -1:
                        x_pos = SCREEN_WIDTH + 100
                    elif enemy.direction == 1:
                        x_pos = -100
                    else:
                        pass
                    if player.score > 200:
                        enemy_sprite = Enemy(x_pos, y_pos, random.choice(['wingman', 'wingman', 'flyman', 'flyman', 'flyman']), random.choice([True, False]))
                        enemy_group.add(enemy_sprite)

            for powerup in powerup_group:
                powerup.update()

            for player in player_single:
                player.update()

                # Check Game over --- Falling 
                if player.rect.top > SCREEN_HEIGHT + 20:
                    game_over_sound.play()
                    game_over = True    

            draw_text('Score:' + str(player.score), 5, 120, 20)
            for i in range(player.health):
                screen.blit(life_img, (i * 30, 20))
            screen.blit(coin_img, (2, 75))
            draw_text('x' + str(player.coin), 45, 80, 20)

        else:
            # Game over screen
            draw_text('Game Over!', 5, 180, 54)
            draw_text('Score:', 100, 290, 60)
            draw_text(str(player.score), 110, 410, 80)
            draw_text("Press S to Restart!", 5, 580, 28)
        
            key = pygame.key.get_pressed()
            if key[pygame.K_s]: # Press S to restart
                screen_sound.play()
                enemy_group.empty()
                platform_group.empty()  
                decoration_group.empty()
                powerup_group.empty()
                game_over = False

                player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)  
                player_single.add(player)

                # Starting position
                start_pos = Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 'ground_grass', False)
                platform_group.add(start_pos)     

                # Testing enemy movement
                sun_img = Enemy(SCREEN_WIDTH - 125, 55, 'sun', False)
                enemy_group.add(sun_img)
                player.score = 0 
                
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Add more difficulty
        if event.type == enemy_timer and player.score > 800:
            enemy_group.add(Enemy(random.randint(50, SCREEN_WIDTH - 50), -250, 'spikeball', True))

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
