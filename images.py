import pygame
import os

from window import WIDTH, HEIGHT
from alien import ALIEN_HEIGHT, ALIEN_WIDTH
from tank import TANK_HEIGHT, TANK_WIDTH

# Background
SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))
# Bottom Level Alien
ALIEN_BOTTOM_IMAGE = pygame.image.load(os.path.join('Assets', 'Alien1.png'))
ALIEN_BOTTOM = pygame.transform.scale(ALIEN_BOTTOM_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))
# Middle Row Alien
ALIEN_MIDDLE_IMAGE = pygame.image.load(os.path.join('Assets', 'Alien2.png'))
ALIEN_MIDDLE = pygame.transform.scale(ALIEN_MIDDLE_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))
# Top Row Alien
ALIEN_TOP_IMAGE = pygame.image.load(os.path.join('Assets', 'Alien3.png'))
ALIEN_TOP = pygame.transform.scale(ALIEN_TOP_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))
# Tank
TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'Tank.png'))
TANK = pygame.transform.scale(TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT))