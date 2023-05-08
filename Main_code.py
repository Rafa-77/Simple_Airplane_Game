import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen (width, height) (x,y)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load(
    r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\background.png")

# Background sound
# mixer.music.load(
#    r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\background.wav")
# mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(
    r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\ufo.png")
pygame.display.set_icon(icon)


# Player
playerimg = pygame.image.load(
    r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\transport.png")
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load(
        r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\enemy.png"))

    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(7)
    enemyY_change.append(50)

# Bullet
bulletimg = pygame.image.load(
    r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\bullet.png")
bulletX = 0
bulletY = playerY
bulletY_change = 7
# Ready - You cant see the bullet on the screen
# Fire - the bullet is currently moving
bullet_state = "Ready"

# Score
score_value = 0
font = pygame.font.Font("C:\\Windows\Fonts\Arial.ttf", 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("C:\\Windows\Fonts\Arial.ttf", 65)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (240, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot((enemyX-bulletX), (enemyY-bulletY))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # Elegir el color de la pantalla
    screen.fill((20, 20, 20))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # is keystroke is pressed chech wheter its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 4.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    bullet_sound = mixer.Sound(
                        r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    # Boundaries for spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # Collition
        collition = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collition:
            collition_sound = mixer.Sound(
                r"C:\\Users\miria\Desktop\Programacion Cuarentena\Pygame tutorial\explosion.wav")
            collition_sound.play()
            bulletY = playerY
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "Ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
