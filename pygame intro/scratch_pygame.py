import random
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite): # (self) here is equals to Player
    def __init__(self):
        super().__init__()# THIS IS IMPORTANT
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]# on the ground animation
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')# Sound
        self.jump_sound.set_volume(0.2)

    def player_input(self):# to check whether keys are being pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):# for player not to fall through under the ground
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:# jumping animation
            self.image = self.player_jump

        else:
            self.player_index += 0.1# changing the animation from animation 1 to animation 2
            if self.player_index >= len(self.player_walk):# to make the player_index from 0-1 to 1-0
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):# this is use to call or use the other functions as one
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':# Fly
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:# Snail
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):# Animation of both snail and fly
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):# to filter out obstacle when it's outside the screen
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

def display_score():
    # global current_time # to access this Variable everywhere
    current_time = int(pygame.time.get_ticks() / 1000)- start_time #to subtract the start_time to current_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):# for the movement of snail
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 # snail move to left

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]# to filter out obstacle when it's outside the screen

        return obstacle_list
    else:
        return []# return empty list so you can .append even though this function has a None value

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():# this is for collision of player and obstacle(sprite,group,bool)
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()# to delete all everything if player and obstacle collide
        return False
    else:
        return True

def player_animation():# for animation of walk and jumping
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):# to make the player_index from 0-1 to 1-0
            player_index = 0
        player_surf = player_walk[int(player_index)]


# THIS IS THE VERY VERY VERY FIRST THING THAT NEED TO DO!!!
pygame.init()# set the screen display (width, height) base on px
screen = pygame.display.set_mode((800, 400))# the title of the game
pygame.display.set_caption('Runner')# to help with adjusting the fps
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)# to make a text (font type, font size)
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.music.load('audio/jazz.mp3')#
pygame.mixer.music.play(-1)# for bg music to loop
pygame.mixer.music.set_volume(0.2)# to set the volume

# Groups
player = pygame.sprite.GroupSingle()# GroupSingle is for a single surface in a Class
player.add(Player())# to add the Player Class

obstacle_group = pygame.sprite.Group()# Group is for multiple surfaces in a Class

sky_surface = pygame.image.load('graphics/Sky.png').convert()# to set the of the surface within the screen(width,height)
ground_surface = pygame.image.load('graphics/ground.png').convert()
# (text, anti-aliase, color)
# score_surf = test_font.render('My game', False, (64,64,64))# used color here is rgb
# score_rect = score_surf.get_rect(center = (400, 50))

# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Obstacle
obstacle_rect_list = []

# Player surface
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))# to get the rectangle of the player_walk_1 Variable | player rectangle (left, top, width, height)
player_gravity = 0 # gravity

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)# (player_surface, angle, scale)
player_stand_rect = player_stand.get_rect(center = (400, 200))# getting the rect of scaled player

# Restart text
game_name = test_font.render('Pixel runner',False,(111, 196, 169))#outro text
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to restart',False,(111, 196, 169))# outro text
game_message_rect = game_message.get_rect(center = (400, 320))

# Timer | to trigger time (event,milliseconds)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)  # Obstacle spawn timer

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)  # Snail animation timer

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)  # Fly animation timer

# to put color on the surface
# test_surface.fill('Red')


while True:# forever loop to actually stop the screen from closing
    for event in pygame.event.get():# for loop to be able to close the game
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()# for music to stop
            pygame.quit()
            exit()# exit() to stop the while loop. this is from Import

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if any mouse button is pressed
                if player_rect.collidepoint(event.pos) and player_rect.bottom:  # Check if the left mouse button (button 1) is pressed to the player rect
                    player_gravity = -20  # Modify player's gravity (example)

            if event.type == pygame.KEYDOWN:# Check if any key is pressed
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:# Check if the spacebar key is pressed
                    player_gravity = -20

        else:# to restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)# score back to 0 when restarted

        if game_active:# timer of obstacles
            if event.type == obstacle_timer : # to have a timer
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))# to change the odds of spawning | so 25% chance of fly and 75% chance of snail
                # if randint(0,2):# to put the obstacle in the screen
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == snail_animation_timer:# animation of snail
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:# animation of fly
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]


        # if event.type == pygame.KEYUP:# to press keyup
        #     print('key up')

    if game_active:# INGAME CODE
        # to put one surface to another surface (surface,position(x and y axis)->px) already have surface Variable -> test_surface||position is to position the Variable
        # +x= right, -x= left, +y= down, -y= up
        screen.blit(sky_surface,(0, 0))#sky
        screen.blit(ground_surface,(0, 300))#ground
        # pygame.draw.rect(screen, '#c0e8ec', score_rect,)#this is the center when using border width below | used color here is hex
        # pygame.draw.rect(screen,'#c0e8ec', score_rect, 10) #rectangle of drawing (display surface, color, the Variable you want to put to, border width)
        # # pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50, 200, 100, 100))#circle | pygame.Rect(left, top, width, height)
        # screen.blit(score_surf, score_rect)#score
        score = display_score()

        # Snail
        # snail_rect.x -=4 #.x means x coord. so -4 for snail to go to left
        # if snail_rect.right <= 0: #check whether the right side of snail is 0 coord
        #     snail_rect.left = 800 #if true, then show the left side of snail to 800 coord
        # screen.blit(snail_surf, snail_rect) #coordinates of snail

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:# to make the player standing on the ground
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf,player_rect) #already assigned the coordinates on the Variable
        player.draw(screen)# to draw the player from the Player Class
        player.update()

        obstacle_group.draw(screen)# to draw the obstacle from the Obstacle Class
        obstacle_group.update()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collision_sprite()
        # game_active = collisions(player_rect,obstacle_rect_list)# the game ended when player_rect touches the obstacle_rect
        # if snail_rect.colliderect(player_rect):# to quit when player touches the snail
        #    game_active = False

    else:# when the game ended
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()# to clear all the obstacle when the game ended
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))# score test
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)# to show title
        else:
            screen.blit(score_message,score_message_rect)# to show score



        # keys = pygame.key.get_pressed()#to press keys
        # if keys[pygame.K_SPACE]:#check the documentation what buttons is needed to be press
        #     print('jump')

        # if player_rect.collidedrect(snail_rect):
            # print('collision')

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #     print('collision')

    pygame.display.update()# this is to update everything to screen Variable
    clock.tick(60)# this is to set the maximum fps