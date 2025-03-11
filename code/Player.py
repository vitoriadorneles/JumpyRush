import pygame

from code.Const import JUMP, WIN_HEIGHT
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

    def update(self):
        if self.jumping:
            if self.rect.y <= 100:
                self.jumping = False
            self.rect.y -= JUMP

        else:
            if self.rect.y < self.initial_position:
                self.rect.y += JUMP
            else:
                self.rect.y = self.initial_position

    def move(self):
        pass
