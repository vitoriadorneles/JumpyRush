import pygame

from code.Const import WIN_HEIGHT, WIN_WIDTH
from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.name = name
        self.position = (25, WIN_HEIGHT - 130)
        self.image = pygame.image.load(f'./assets/{name}.png')
        self.rect = self.image.get_rect(topleft=position)

        self.animation_time = 1
        self.animation_speed = 50

        self.jumping = False
        self.initial_position = (WIN_HEIGHT - 130)

    def jump(self):
        self.jumping = True

    def updateJump(self):
        if self.jumping:
            if self.rect.y <= 80:
                self.jumping = False
            self.rect.centery -= 7

        else:
            if self.rect.y < self.initial_position:
                self.rect.y += 7
            else:
                self.rect.y = self.initial_position

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.centerx -= 5
        if pressed_key[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += 5

