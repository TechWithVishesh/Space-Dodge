import pygame
import time
import random
pygame.font.init()

FPS = 60

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("Background.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 60, 100
PLAYER = pygame.transform.scale(pygame.image.load("Player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

PLAYER_VEL = 5

FONT = pygame.font.SysFont("timesnewroman", 40)
FONT1 = pygame.font.SysFont("algerian", 100)

LASER_WIDTH, LASER_HEIGHT = 10, 30
LASER_VEL = 3

def draw(player, elapsed_time, lasers, lives):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    WIN.blit(PLAYER, (player.x, player.y))
    
    for laser in lasers:
        pygame.draw.rect(WIN, "red", laser)

    time_text = FONT.render(f"Time: {round(elapsed_time)} s", 1, "white")
    WIN.blit(time_text, (10, 10))

    Lives = FONT.render(f"Lives: {lives}", 1, "white")
    WIN.blit(Lives, (15, 45))

    pygame.display.update()

def main():
    run = True

    player  = pygame.Rect((450, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
    
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0
    lives = 5

    laser_add_increment = 2000
    laser_count = 0

    lasers = []

    while run:
        laser_count += clock.tick(FPS)
        elapsed_time = time.time() - start_time

        if laser_count > laser_add_increment:
            for _ in range(2):
                laser_x = random.randint(0, WIDTH - LASER_WIDTH)
                laser = pygame.Rect(laser_x, -LASER_HEIGHT, LASER_WIDTH, LASER_HEIGHT)
                lasers.append(laser)

            laser_add_increment = max(400, laser_add_increment - 100)
            laser_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for laser in lasers[:]:
            laser.y += LASER_VEL
            if laser.y > HEIGHT:
                lasers.remove(laser)
            elif laser.y + LASER_HEIGHT >= player.y and laser.colliderect(player):
                lasers.remove(laser)
                lives -= 1

        if lives <= 0:
            lost_text = FONT1.render("YOU LOST!!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, lasers, lives)

    pygame.quit()

if __name__ == "__main__":
    main()