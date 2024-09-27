import pygame
import os
import random

from window import WIN, WIDTH, HEIGHT
from images import SPACE, ALIEN_BOTTOM, ALIEN_MIDDLE, ALIEN_TOP, TANK
from alien import ALIEN_HEIGHT, ALIEN_WIDTH, ALIEN_PADDING, ALIEN_BOTTOM_HEIGHT, ALIEN_DROP_HEIGHT, ALIENS_PER_ROW, REVERSE_DIRECTION_WIDTH
from tank import TANK_WIDTH, TANK_HEIGHT, TANK_VEL, MAX_BULLETS, TANK_LIVES
pygame.font.init()

GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
LIVES_FONT = pygame.font.SysFont('comicsans', 36)

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TANK_BULLET_VEL = 5
ALIEN_BULLET_VEL = 3
BULLET_FIRE_SPEED = 1000

BRIGADE_FIRE = pygame.USEREVENT + 1
TANK_HIT = pygame.USEREVENT + 2
ALIEN_HIT = pygame.USEREVENT + 3

FPS = 60

def draw_window(alien_brigade, alien_bullets, tank, tank_bullets, lives_remaining, score):
    # Draw the background
    WIN.blit(SPACE, (0, 0))
    top_bg = pygame.Rect(0, 0, WIDTH, 70)
    pygame.draw.rect(WIN, BLACK, top_bg)
    # Draw score
    score_text = LIVES_FONT.render(f"Score: {score}", 1, WHITE)
    WIN.blit(score_text, (10, 10))                           
    # Draw the tank
    WIN.blit(TANK, (tank.x, tank.y))
    # Keep track of the tank lives
    draw_text = LIVES_FONT.render("Lives:", 1, WHITE)
    WIN.blit(draw_text, (WIDTH - TANK_LIVES*TANK_WIDTH - 150, 10))
    for life in range(lives_remaining):
        WIN.blit(TANK, (WIDTH - (TANK_LIVES-life)*(TANK_WIDTH + 10), 10))
    # Draw the aliens on the screen
    bottom_aliens, middle_aliens, top_aliens = alien_brigade
    for alien in bottom_aliens:
        WIN.blit(ALIEN_BOTTOM, (alien.x, alien.y))
    for alien in middle_aliens:
        WIN.blit(ALIEN_MIDDLE, (alien.x, alien.y))
    for alien in top_aliens:
        WIN.blit(ALIEN_TOP, (alien.x, alien.y))
    # Draw the bullets as they are fired
    for bullet in tank_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in alien_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()

def move_brigade_down(alien_brigade, direction):

    for row in alien_brigade:
        for alien in row:
            alien.y += ALIEN_DROP_HEIGHT
            alien.x += 5*direction

def handle_alien_moves(alien_brigade, direction):

    # ToDo - fix up the implementation of this function
    bottom_aliens, middle_aliens, top_aliens = alien_brigade
    # bottom_left_alien = bottom_aliens[0]
    # bottom_right_alien = bottom_aliens[-1]

    for row in alien_brigade:
        for alien in row:
            if alien.x < REVERSE_DIRECTION_WIDTH or alien.x > WIDTH - REVERSE_DIRECTION_WIDTH - ALIEN_WIDTH:
                direction *= -1
                move_brigade_down(alien_brigade, direction)
                break
            alien.x += direction
            

    return direction

def create_alien_brigade():

    alien_space = ALIEN_WIDTH + ALIEN_PADDING
    alien_col_height = ALIEN_HEIGHT + ALIEN_PADDING
    # Calculating the position of the alien row dynamically
    alien_start_width = (WIDTH - (alien_space*ALIENS_PER_ROW - ALIEN_PADDING))//2

    bottom_aliens = []
    for width in range(alien_start_width, 
                       alien_start_width + alien_space*ALIENS_PER_ROW,
                       alien_space):
        new_bottom_alien = pygame.Rect(width, ALIEN_BOTTOM_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT)
        bottom_aliens.append(new_bottom_alien)

    middle_aliens = []
    for width in range(alien_start_width, 
                    alien_start_width + alien_space*ALIENS_PER_ROW,
                    alien_space):
        new_middle_alien_row_1 = pygame.Rect(width, ALIEN_BOTTOM_HEIGHT - alien_col_height, ALIEN_WIDTH, ALIEN_HEIGHT)
        new_middle_alien_row_2 = pygame.Rect(width, ALIEN_BOTTOM_HEIGHT - 2*alien_col_height, ALIEN_WIDTH, ALIEN_HEIGHT)
        middle_aliens.append(new_middle_alien_row_1)
        middle_aliens.append(new_middle_alien_row_2)

    top_aliens = []
    for width in range(alien_start_width, 
                alien_start_width + alien_space*ALIENS_PER_ROW,
                alien_space):
        new_top_alien_row_1 = pygame.Rect(width, ALIEN_BOTTOM_HEIGHT - 3*alien_col_height, ALIEN_WIDTH, ALIEN_HEIGHT)
        new_top_alien_row_2 = pygame.Rect(width, ALIEN_BOTTOM_HEIGHT - 4*(ALIEN_HEIGHT + ALIEN_PADDING), ALIEN_WIDTH, ALIEN_HEIGHT)
        top_aliens.append(new_top_alien_row_1)
        top_aliens.append(new_top_alien_row_2)

    alien_brigade = (bottom_aliens, middle_aliens, top_aliens)
    return alien_brigade

def handle_tank_moves(keys_pressed, tank):

    if keys_pressed[pygame.K_LEFT]: #LEFT
        if tank.x - TANK_VEL > 0:
            tank.x -= TANK_VEL
    if keys_pressed[pygame.K_RIGHT]: # RIGHT
        if tank.x + TANK_VEL + tank.width < WIDTH:
            tank.x += TANK_VEL

def handle_bullets(tank_bullets, alien_bullets, tank, alien_brigade):
    
    for bullet in tank_bullets:
        bullet.y -= TANK_BULLET_VEL
        if bullet.y <= 0:
            tank_bullets.remove(bullet)
        for row in alien_brigade:
            for alien in row:
                if alien.colliderect(bullet):
                    tank_bullets.remove(bullet)
                    pygame.event.post(pygame.event.Event(ALIEN_HIT))
                    row.remove(alien)

    for bullet in alien_bullets:
        bullet.y += ALIEN_BULLET_VEL
        if tank.colliderect(bullet):
            alien_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(TANK_HIT))
            print("Life Lost !")

def draw_game_won():

    draw_text = GAME_OVER_FONT.render("You Won !", 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_game_over():
    draw_text = GAME_OVER_FONT.render("Game Over!", 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    alien_brigade = create_alien_brigade()
    tank = pygame.Rect((WIDTH - TANK_WIDTH)//2, HEIGHT - TANK_HEIGHT - 20, TANK_WIDTH, TANK_HEIGHT)
    tank_bullets = []
    alien_bullets = []

    score = 0

    lives_remaining = TANK_LIVES

    clock = pygame.time.Clock()
    run = True

    pygame.time.set_timer(BRIGADE_FIRE, BULLET_FIRE_SPEED)

    direction = 1

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == BRIGADE_FIRE:
                # ToDo: handle when there are no aliens left
                remaining_rows = [row for row in alien_brigade if row]
                try:
                    rand_alien_row = random.choice(remaining_rows)
                    rand_alien = random.choice(rand_alien_row)
                    bullet = pygame.Rect(rand_alien.x + rand_alien.width //2, rand_alien.y, 10, 5)
                    alien_bullets.append(bullet)
                except IndexError:
                    draw_game_won()
                    run = False
            if event.type == TANK_HIT:
                lives_remaining -= 1
            if event.type == ALIEN_HIT:
                score += 10
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(tank_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(tank.x + tank.width//2, tank.y, 10, 5)
                    tank_bullets.append(bullet)

        if lives_remaining == 0:
            draw_game_over()
            run = False
                
        direction = handle_alien_moves(alien_brigade, direction)
        keys_pressed = pygame.key.get_pressed()
        handle_tank_moves(keys_pressed, tank)
        handle_bullets(tank_bullets, alien_bullets, tank, alien_brigade)
        draw_window(alien_brigade, alien_bullets, tank, tank_bullets, lives_remaining, score)

    
    pygame.quit()

if __name__ == "__main__":
    main()