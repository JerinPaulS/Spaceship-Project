import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle Duo")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
AMBER = (255, 255, 0)
RED = (255, 0, 0)
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

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
INTRO_FONT = pygame.font.SysFont('freesansbold.ttf',115)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Shot.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Fire.wav'))

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


def draw_window(sp1, sp2, sp1_bullets, sp2_bullets, sp1_health, sp2_health):
    WIN.blit(SPACE, (0, 0))
    if sp1_health < 7 and sp1_health > 4:
        SCORE_COLOR_SP1 = AMBER
    elif sp1_health <= 4:
        SCORE_COLOR_SP1 = RED
    else:
        SCORE_COLOR_SP1 = GREEN
    if sp2_health < 7 and sp2_health > 4:
        SCORE_COLOR_SP2 = AMBER
    elif sp2_health <= 4:
        SCORE_COLOR_SP2 = RED
    else:
        SCORE_COLOR_SP2 = GREEN
    pygame.draw.rect(WIN, SCORE_COLOR_SP1, (0, 0, sp1_health * 45, 8))
    pygame.draw.rect(WIN, SCORE_COLOR_SP2, (WIDTH - sp2_health * 45, 0, sp2_health * 45, 8))
    pygame.draw.rect(WIN, BLACK, BORDER)

    sp1_health_text = HEALTH_FONT.render("Health: " + str(sp1_health), 1, WHITE)
    sp2_health_text = HEALTH_FONT.render("Health: " + str(sp2_health), 1, WHITE)

    WIN.blit(sp1_health_text, (10, 10))
    WIN.blit(sp2_health_text, (WIDTH - sp2_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (sp1.x, sp1.y))
    WIN.blit(RED_SPACESHIP, (sp2.x, sp2.y))

    for bullet in sp1_bullets:
        pygame.draw.rect(WIN, SP1_COLOR, bullet)
    for bullet in sp2_bullets:
        pygame.draw.rect(WIN, SP2_COLOR, bullet)
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(WHITE)
        draw_text = INTRO_FONT.render("SPACE SHIP DUEL", 1, BLACK)
        WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))

        pygame.draw.rect(WIN, GREEN, (150,450,100,50))
        pygame.draw.rect(WIN, RED, (550,450,100,50))

        pygame.display.update()
        pygame.time.delay(5000)

def main():
    clock = pygame.time.Clock()
    run = True
    sp1 = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    sp2 = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    sp1_bullets = []
    sp2_bullets = []

    sp1_health = 10
    sp2_health = 10

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(sp1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(sp1.x + sp1.width, sp1.y + sp1.height // 2 - 2, 10, 5)
                    sp1_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(sp2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(sp2.x, sp2.y + sp2.height // 2 - 2, 10, 5)
                    sp2_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == SP1_HIT:
                sp1_health = sp1_health - 1
                BULLET_HIT_SOUND.play()
            if event.type == SP2_HIT:
                sp2_health = sp2_health - 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if sp1_health <= 0:
            winner_text = "Player 2 wins!"
        if sp2_health <= 0:
            winner_text = "Player 1 wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        spship1_handle_movement(keys_pressed, sp1)
        spship2_handle_movement(keys_pressed, sp2)
        handle_bullets(sp1_bullets, sp2_bullets, sp1, sp2)

        draw_window(sp1, sp2, sp1_bullets, sp2_bullets, sp1_health, sp2_health)

    main()

if __name__ == "__main__":
    game_intro()
    main()
