import pygame

from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.image = pygame.image.load(f'./assets/{name}.png')
        self.rect = self.image.get_rect(topleft=position)
        self.animation_time = 1
        self.animation_speed = 100

        self.gravity = 0
        self.jump_count = 0
        self.is_jumping = False

    def update(self):
        pass

    def move(self):
        pass
