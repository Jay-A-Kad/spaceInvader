import pygame
import random
import math

#  Initializer the pygame
pygame.init()
pygame.font.init()
# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# title and icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load('planet.png')
pygame.display.set_icon(icon)


# player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy alien
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(1)

# sword ready--cannot see bullet on screen and fire when moving
swordImg = pygame.image.load('sword.png')
swordX = 0
swordY = 480
swordX_change = 0
swordY_change = 10
sword_state = "ready"

score = 0


# setting score
font = pygame.font.Font('ARIAL.ttf', 48)


def show_score(x, y):
    score_value = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_sword(x, y):
    global sword_state
    sword_state = "fire"
    screen.blit(swordImg, (x + 16, y + 10))


def isCollison(enemyX, enemyY, swordX, swordY):
    distance = math.sqrt((math.pow(enemyX - swordX, 2)) +
                         (math.pow(enemyY - swordY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Space Invaders closed...")

        # if keyboard is pressed move left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if sword_state == "ready":
                    swordX = playerX
                    fire_sword(swordX, swordY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # left right increment logic
    playerX += playerX_change

    # space ship boundary logic
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement and collision detection
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollison(enemyX[i], enemyY[i], swordX, swordY)
        if collision:
            swordY = 480
            sword_state = "ready"
            score += 1
            print(score)

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # sword movement
    if swordY <= 0:
        swordY = 480
        sword_state = "ready"
    if sword_state == "fire":
        fire_sword(swordX, swordY)
        swordY -= swordY_change

    player(playerX, playerY)
    show_score(10, 10)

    pygame.display.update()
