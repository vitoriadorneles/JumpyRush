# B
import pygame

BTN_SIZE = (150, 50)

# C
C_PURPLE = (90, 13, 156)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)

# E
EVENT_OBSTACLE = pygame.USEREVENT + 1

ENTITY_SPEED = {
    'Level1Bg0': 1,
    'Level1Bg1': 3,
    'Level1Bg2': 4,
    'Level1Bg3': 5,
    'Obstacle1Img0': 2,
    'Obstacle1Img1': 2,
    'Obstacle2Img0': 2,
    'Obstacle2Img1': 2,
    'Obstacle2Img2': 2,
    'Obstacle2Img3': 2,
}
ENTITY_HEALTH = {
    'Player': 200,
    'PlayerImg0': 200,
    'PlayerImg1': 200,
    'PlayerImg2': 200,
    'PlayerImg3': 200,
    'PlayerImg4': 200,
    'PlayerImg5': 200,
    'PlayerImg6': 200,
    'PlayerImg7': 200,
    'Obstacle1Img0': 50,
    'Obstacle1Img1': 60,
    'Obstacle2Img0': 50,
    'Obstacle2Img1': 50,
    'Obstacle2Img2': 50,
    'Obstacle2Img3': 50,
    'Level1Bg0': 999,
    'Level1Bg1': 999,
    'Level1Bg2': 999,
    'Level1Bg3': 999,
}

ENTITY_DAMAGE = {
    'Player': 200,
    'PlayerImg0': 10,
    'PlayerImg1': 10,
    'PlayerImg2': 10,
    'PlayerImg3': 10,
    'PlayerImg4': 10,
    'PlayerImg5': 10,
    'PlayerImg6': 10,
    'PlayerImg7': 10,
    'Obstacle1Img0': 20,
    'Obstacle1Img1': 100,
    'Obstacle2Img0': 15,
    'Obstacle2Img1': 15,
    'Obstacle2Img2': 15,
    'Obstacle2Img3': 15,
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
}



# M
MENU_OPTION = ('NEW GAME', 'SCORE', 'EXIT',)

# P
PLAYER_IMG = [
    'PlayerImg0',
    'PlayerImg0',
    'PlayerImg0',
    'PlayerImg0',
    'PlayerImg0',
    'PlayerImg0',
]

# W
WIN_WIDTH = 576
WIN_HEIGHT = 324
