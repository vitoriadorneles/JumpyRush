import pygame

from code.Const import ENTITY_SPEED, WIN_WIDTH, WIN_HEIGHT
from code.Entity import Entity


class Obstacle(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.name = name

        self.image = pygame.image.load(f'./assets/{name}.png').convert_alpha()
        self.rect = self.image.get_rect(topright=position)

    def move(self):
        self.rect.centerx -= 5
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH

    def update(self):
        pass
