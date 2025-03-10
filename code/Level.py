import sys

import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import C_PURPLE, WIN_HEIGHT
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Player import Player


class Level:
    def __init__(self, window, name, game):
        self.window = window
        self.name = name
        self.game = game
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.timeout = 2000

        self.player_images = EntityFactory.get_entity("PlayerImg")
        self.current_player_image_index = 0
        self.animation_counter = 0

    def run(self, ):
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update the player animation index
            self.animation_counter += 3
            if self.animation_counter > 25:
                self.animation_counter = 0
                self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

            current_player = self.player_images[self.current_player_image_index]
            self.window.blit(current_player.image, current_player.rect.topleft)

            pygame.display.flip()

            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000: .1f}s', C_PURPLE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps() :0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()

            pass

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
