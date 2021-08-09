import pygame
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle Duo")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
MAX_BULLETS = 3
SPACESHIP_WIDTH = 65
SPACESHIP_HEIGHT = 60
VEL = 5
BULLET_VEL = 7
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 7, HEIGHT)
SP1_HIT = pygame.USEREVENT + 1
SP2_HIT = pygame.USEREVENT + 2
SP1_COLOR = (255, 255, 0)
SP2_COLOR = (255, 0, 0)

SPACE = pygame.image.load(os.path.join('Assets', 'space.jpg'))
YELLOW_SPACESHIP = pygame.image.load(os.path.join('Assets', 'yellowspaceship.png'))
#BLUE_SPACESHIP = pygame.image.load(os.path.join('Assets', 'bluespaceship.png'))
#GREEN_SPACESHIP = pygame.image.load(os.path.join('Assets', 'greenspaceship.png'))
RED_SPACESHIP = pygame.image.load(os.path.join('Assets', 'redspaceship.png'))

SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
#BLUE_SPACESHIP = pygame.transform.scale(BLUE_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
#GREEN_SPACESHIP = pygame.transform.scale(GREEN_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

def spship1_handle_movement(keys_pressed, sp1):
    if keys_pressed[pygame.K_a] and sp1.x - VEL > 0:
        sp1.x = sp1.x - VEL
    if keys_pressed[pygame.K_d] and sp1.x + sp1.width + VEL < BORDER.x:
        sp1.x = sp1.x + VEL
    if keys_pressed[pygame.K_s] and sp1.y + sp1.height + VEL < HEIGHT:
        sp1.y = sp1.y + VEL
    if keys_pressed[pygame.K_w] and sp1.y - VEL > 0:
        sp1.y = sp1.y - VEL

def spship2_handle_movement(keys_pressed, sp2):
    if keys_pressed[pygame.K_LEFT] and sp2.x - VEL > BORDER.x + BORDER.width:
        sp2.x = sp2.x - VEL
    if keys_pressed[pygame.K_RIGHT] and sp2.x + sp2.width + VEL < WIDTH:
        sp2.x = sp2.x + VEL
    if keys_pressed[pygame.K_DOWN] and sp2.y + sp2.height + VEL < HEIGHT:
        sp2.y = sp2.y + VEL
    if keys_pressed[pygame.K_UP] and sp2.y - VEL > 0:
        sp2.y = sp2.y - VEL

def handle_bullets(sp1_bullets, sp2_bullets, sp1, sp2):
    for bullet in sp1_bullets:
        bullet.x = bullet.x + BULLET_VEL
        if sp2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SP2_HIT))
            sp1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            sp1_bullets.remove(bullet)

    for bullet in sp2_bullets:
        bullet.x = bullet.x - BULLET_VEL
        if sp1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SP1_HIT))
            sp2_bullets.remove(bullet)
        elif bullet.x < 0:
            sp2_bullets.remove(bullet)


def draw_window(sp1, sp2, sp1_bullets, sp2_bullets):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (sp1.x, sp1.y))
    WIN.blit(RED_SPACESHIP, (sp2.x, sp2.y))
    for bullet in sp1_bullets:
        pygame.draw.rect(WIN, SP1_COLOR, bullet)
    for bullet in sp2_bullets:
        pygame.draw.rect(WIN, SP2_COLOR, bullet)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    sp1 = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    sp2 = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    sp1_bullets = []
    sp2_bullets = []

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(sp1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(sp1.x + sp1.width, sp1.y + sp1.height // 2 - 2, 10, 5)
                    sp1_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(sp2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(sp2.x, sp2.y + sp2.height // 2 - 2, 10, 5)
                    sp2_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        spship1_handle_movement(keys_pressed, sp1)
        spship2_handle_movement(keys_pressed, sp2)
        handle_bullets(sp1_bullets, sp2_bullets, sp1, sp2)

        draw_window(sp1, sp2, sp1_bullets, sp2_bullets)

    pygame.quit()

if __name__ == "__main__":
    main()
