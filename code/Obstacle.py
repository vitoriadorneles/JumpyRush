import pygame

from code.Entity import Entity


class Obstacle(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.name = name
        self.image = pygame.image.load(f'./assets/{name}.png').convert_alpha()
        self.rect = self.image.get_rect(topright=position)
        self.speed = 5  # Velocidade inicial do obstáculo

        # Criação da máscara para detecção pixel a pixel
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.centerx -= self.speed  # Move o obstáculo para a esquerda
