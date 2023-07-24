import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# Load game assets
background_image = pygame.image.load("background.jpeg")
background_image = pygame.transform.scale(background_image, (800, 600))

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (64, 64)) 

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (64, 64))  

bullet_image = pygame.image.load("bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (26, 26))  

explosion_image = pygame.image.load("explosion.png")
explosion_image = pygame.transform.scale(explosion_image, (64, 64))  


BLACK = (0, 0, 0)


player_x = width // 2 - 32
player_y = height - 100
player_speed = 5


bullet_x = 0
bullet_y = height
bullet_speed = 10
bullet_state = "ready"


num_enemies = 6
enemy_x = []
enemy_y = []
enemy_speed = []
for i in range(num_enemies):
    enemy_x.append(random.randint(0, width - 64))
    enemy_y.append(random.randint(50, 200))
    enemy_speed.append(2)


score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_x += player_speed
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x + 16
                    bullet_y = player_y
                    bullet_state = "fire"

    # Update player position
    if player_x < 0:
        player_x = 0
    elif player_x > width - 64:
        player_x = width - 64

    # Update bullet position
    if bullet_y <= 0:
        bullet_y = height
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet_y -= bullet_speed

    # Update enemy position
    for i in range(num_enemies):
        enemy_x[i] += enemy_speed[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= width - 64:
            enemy_speed[i] = -enemy_speed[i]
            enemy_y[i] += 40

        # Check for collision
        if (
            bullet_x >= enemy_x[i]
            and bullet_x <= enemy_x[i] + 64
            and bullet_y <= enemy_y[i] + 64
        ):
            score += 1
            bullet_y = height
            bullet_state = "ready"
            enemy_x[i] = random.randint(0, width - 64)
            enemy_y[i] = random.randint(50, 200)

    
    
    # Draw the game elements
    window.blit(background_image, (0, 0))
    window.blit(player_image, (player_x, player_y))
    if bullet_state == "fire":
        window.blit(bullet_image, (bullet_x, bullet_y))

    for i in range(num_enemies):
        window.blit(enemy_image, (enemy_x[i], enemy_y[i]))

    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (text_x, text_y))

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()

