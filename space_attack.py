"""
Space attack Game
Using Pygame
Created on Sun Apr  5 13:26:05 2020

@author: Biswaraj
"""
import pygame
from pygame import mixer
import random
import math

pygame.init()

screen_width = 800
screen_height = 600

# Create Screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
backgroundImg = pygame.image.load('bg.jpg')

# Background Music
# -1 is to play the music on loop

# Remove the comment from below two lines to play Background Music.

# mixer.music.load('background.wav')
# mixer.music.play(-1)


# Caption and Logo
pygame.display.set_caption('Space Attack')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player Spaceship
playerImg = pygame.image.load ('player_spaceship.png')
playerX = screen_width/2 - 64
playerY = screen_height/2 + 200
playerSpeed = 4


# Enemy Alien
AlienImg = []
alienX = []
alienY = []
alienXchange = []
alienYchange = []
alienSpeed = []
no_of_aliens = 6

for i in range(no_of_aliens):
    AlienImg.append(pygame.image.load ('alien.png'))
    # Load alien image in random locations.
    alienX.append(random.randint(10, 730))
    alienY.append(random.randint(12, 80))
    alienXchange.append(3.5)
    alienYchange.append(30)
    alienSpeed.append(3)

# bullet
bulletImg = pygame.image.load ('bullet.png')
bulletX = screen_width/2 - 64
bulletY = screen_height/2 + 200 - 10
bulletXchange = 0
bulletYchange = 10
isfiring = False

# Score
scoreValue = 0
textX = 10
textY = 10
font = pygame.font.Font('COVID-SY.otf', 32)

# game over
game_over_font = pygame.font.Font('COVID-SY.otf', 64)
gameOverX = screen_width/2
gameOverY = screen_height/2
isgameOver = False

def display_score(x, y):
    score = font.render('Score : ' + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))
    
def player(x, y):
    screen.blit(playerImg, (x, y))

def alien(x, y, i):
    screen.blit(AlienImg[i], (x, y))

def bullet_fire(x, y):
    global isfiring
    isfiring = True
    screen.blit(bulletImg, (x, y))

def isCollision(X1, Y1, X2, Y2):
    distance = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)
    if distance <= 30:
        return True

def game_over():
    gameOver = game_over_font.render('Game Over', True, (255 ,255 ,255))
    screen.blit(gameOver, (220, 200))

# Game Loop
run = True
while run:
    screen.fill((0,0,0))
    # Background Image
    screen.blit(backgroundImg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE and isfiring == False:
                firingSound = mixer.Sound('laser.wav')
                firingSound.play()
                bulletX = playerX
                bullet_fire(bulletX, bulletY)
                
    
    keys = pygame.key.get_pressed()
    
    # Player Movement
    if keys[pygame.K_RIGHT] and playerX < screen_width - 64:
        playerX += playerSpeed
    elif keys[pygame.K_LEFT] and playerX > 0:
        playerX -= playerSpeed
    
    # Alien Movement
    for i in range(no_of_aliens):
        # game over
        if alienY[i] >= 440:
            for j in range(no_of_aliens):
                alienY[j] = -2000
                isgameOver = True
        if isgameOver:
            game_over()
            
            
        alienX[i] += alienXchange[i]
        # If hits the boundary move to left/right and move down by 30 units.
        if alienX[i] <= 0:
            alienXchange[i] = alienSpeed[i]
            alienY[i] += alienYchange[i]
        elif alienX[i] >= screen_width - 64:
            alienXchange[i] = -alienSpeed[i]
            alienY[i] += alienYchange[i]
            

        # Collision
        if isCollision(alienX[i], alienY[i], bulletX, bulletY):
            collisionSound = mixer.Sound('explosion.wav')
            collisionSound.play()
            bulletY = screen_height/2 + 200 - 10
            alienY[i] = -2000
            isfiring = False
            scoreValue += 1
            alienX[i] = random.randint(5, 730)
            alienY[i] = random.randint(5, 80)
            
        alien(alienX[i], alienY[i], i)
    
    
    # Bullet Movement
    if isfiring:
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletYchange
        if bulletY <= 0:
            isfiring = False
            bulletX = screen_width/2 - 64
            bulletY = screen_height/2 + 200 - 10
    
    
    display_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
    

pygame.quit()