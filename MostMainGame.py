import pygame
import random
import math
from pygame import mixer

pygame.init()
# width , height
screen = pygame.display.set_mode((800, 600))
# sets the title
pygame.display.set_caption("First Window")
# sets the icon like in tkinter
#icon = pygame.image.load('E:\\hotel-icon.png')
#pygame.display.set_icon(icon)
# setting background
bg = pygame.image.load('E:\\4Z_2104.w028.n002.36B.p30.36.png')

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# setting player
playerimg = pygame.image.load('C:\\Users\\Salik Pasha\\Downloads\\icons8-space-fighter-80.png')
# X and Y are the coordinates to place the image(space ship)
playerX = 350
playerY = 400
x_change = 0

#enemies images and starting positions
enemyimg = pygame.image.load('C:\\Users\\Salik Pasha\\Downloads\\icons8-enemy-32.png')
# X and Y are the coordinates to place the image
enemyX = random.randint(0, 720)
enemyY = random.randint(50, 150)
ex_change = 0.5
ey_change = 40

#array to create  a number of enemies
enemyimg = []
enemyX = []
enemyY = []
ex_change = []
ey_change = []
num_of_enemies = 20
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('C:\\Users\\Salik Pasha\\Downloads\\icons8-enemy-32.png'))
    enemyX.append(random.randint(0, 720))
    enemyY.append(random.randint(50, 150))
    ex_change.append(0.5)
    ey_change.append(40)

# ready - bullet is not moving
# fire - bullet moves on screen
bullet = pygame.image.load('C:\\Users\\Salik Pasha\\Downloads\\icons8-bullet-32.png')
# X and Y are the coordinates to place the image
bulletX = random.randint(0, 800)
bulletY = 480
bx_change = 0
by_change = 15
b_state = "ready"

# calculates the score of the player
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10
#game over text
over = font = pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def player(x, y):  # blit means to draw,2 parameters
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):  # blit means to draw,2 parameters
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global b_state
    b_state = "fire"
    screen.blit(bullet, (x + 25, y - 80))  # x+16,y+10 makes the bullet to appear above spaceship


def collide(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


done = False
while not done:
    # setting the background  RGB(red,green,blue) implement the colour on screen (values are 0-255)
    screen.fill((0, 0, 0))
    # background image
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # checking keystroke if they are left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -0.3
            if event.key == pygame.K_RIGHT:
                x_change = 0.3
            if event.key == pygame.K_SPACE:
                if b_state == "ready":
                    b_sound = mixer.Sound('laser.wav')
                    b_sound.play()
                    # bullet gets x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

            # checking when keystroke is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0

    # setting boundaries of spaceship and enemy
    playerX += x_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 720:
        playerX = 720
    for i in range(num_of_enemies):
        #Game over code
        if enemyY[i] > 440 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += ex_change[i]
        if enemyX[i] <= 0:
            ex_change[i] = 0.7
            enemyY[i] += ey_change[i]
        elif enemyX[i] >= 720:
            ex_change[i] = -0.7
            enemyY[i] += ey_change[i]
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            c_sound = mixer.Sound('explosion.wav')
            c_sound.play()
            bulletY = 480
            b_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 720)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        b_state = "ready"

    if b_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= by_change

    # check for collision

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()