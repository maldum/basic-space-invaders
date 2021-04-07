import sys
import pygame
import random
import math
from pygame import mixer #for sounds

#initialize pygame library
pygame.init() 

#create the screen
size = width, height = 800, 600
screen = pygame.display.set_mode((size))

#background, title and the icon of the game
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load("images/background.png")

#sounds settings
mixer.music.load("sounds/main_theme.wav")
mixer.music.play(-1) #-1 for sound loop


#player settings
player_img = pygame.image.load('images/ship.png')
player_position_x = 370
player_position_y = 480
player_position_x_update = 0

def player(x, y):
    screen.blit(player_img, (x, y))

#alien settings
alien_img = []
alien_position_x =[]
alien_position_y = []
alien_position_x_update = []
alien_position_y_update = []
num_of_aliens = 6

for i in range(num_of_aliens):

    alien_img.append(pygame.image.load("images/alien.png"))
    alien_position_x.append(random.randint(0, 735))
    alien_position_y.append(0)
    alien_position_x_update.append(2)
    alien_position_y_update.append(20)

def alien(x, y, i):
    screen.blit(alien_img[i], (x, y))

#bullet settings
bullet_img = pygame.image.load("images/bullet.png")
bullet_position_x = 0
bullet_position_y = 480
bullet_position_x_update = 0
bullet_position_y_update = 5
bullet_fire_state = False #bullet is not visible

def fire_bullet(x, y):
    global bullet_fire_state
    bullet_fire_state = True
    screen.blit(bullet_img, (x + 16, y + 10)) #bullet appear in the center of the spaceship

def isCollision(alien_position_x, alien_position_y, bullet_position_x, bullet_position_y):
    #distance between two points formula (x1,y1) and (x2,y2)
    distance = math.sqrt(math.pow(alien_position_x - bullet_position_x, 2) + (math.pow(alien_position_y - bullet_position_y,2)))
    if distance < 27:
        return True
    else:
        return False

#score settings

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 18)

def display_score(x = 10, y = 10):
    score = font.render("Score " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

#display "Game Over"
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))



#game loop
while True:

    #setting background color and image
    screen.fill((0, 0, 0))
    screen.blit(background,(0, 0))

    

    for event in pygame.event.get():
        

        if event.type == pygame.QUIT: 
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_position_x_update = -3

            if event.key == pygame.K_RIGHT:
                player_position_x_update = 3
            
            if event.key == pygame.K_SPACE:
                if bullet_fire_state == False:
                    firing_sounds = mixer.Sound("sounds/bullet.wav")
                    firing_sounds.play() 
                    #get the current x position of the spaceship
                    bullet_position_x = player_position_x
                    fire_bullet(bullet_position_x, bullet_position_y)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_position_x_update = 0
    
    #check if the player touch screen edges
    if player_position_x <= 0:
        player_position_x = 0
    elif player_position_x >= 735:
        player_position_x = 735

    player_position_x += player_position_x_update

    player(player_position_x, player_position_y)


    #alien movements
    for i in range(num_of_aliens):
        # game over settings
        if alien_position_y[i] > 440:
            for j in range(num_of_aliens):
                alien_position_y[i] = 2000
            game_over()
            break

        alien_position_x[i] += alien_position_x_update[i]
        if alien_position_x[i] <= 0:
            alien_position_x_update[i] = 2
            alien_position_y[i] += alien_position_y_update[i]
        elif alien_position_x[i] >= 735:
            alien_position_x_update[i] = -2
            alien_position_y[i] += alien_position_y_update[i]
        
         #bullet collision
        collision = isCollision(alien_position_x[i], alien_position_y[i], bullet_position_x, bullet_position_y)

        if collision:
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.play()
            bullet_position_y = 480
            bullet_fire_state = False
            score_value += 1
            alien_position_x[i] = random.randint(0, 735)
            

        alien(alien_position_x[i], alien_position_y[i], i)

    #bullet firing 
    if bullet_position_y < 0:
        bullet_position_y = 480
        bullet_fire_state = False

    if bullet_fire_state:
        fire_bullet(bullet_position_x, bullet_position_y)
        bullet_position_y -= bullet_position_y_update

   
    display_score()

    pygame.display.update()

