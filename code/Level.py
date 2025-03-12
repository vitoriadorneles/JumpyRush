import random
import sys
import time

import pygame.display
from pygame import Surface, Rect, KEYDOWN, K_SPACE
from pygame.font import Font

from code.Const import C_PURPLE, WIN_HEIGHT, WIN_WIDTH, EVENT_OBSTACLE
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window, name, game):
        self.window = window
        self.name = name
        self.game = game
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.timeout = 1000

        self.player_images = EntityFactory.get_entity("PlayerImg")
        self.player = Player("PlayerImg0", (25, WIN_HEIGHT - 130))
        self.current_player_image_index = 0
        self.animation_counter = 0


        self.obstacle2_images = EntityFactory.get_entity("Obstacle2Img")  # Lista de imagens
        self.current_obstacle2_image_index = 0
        self.obstacle2_animation_counter = 0

        pygame.time.set_timer(EVENT_OBSTACLE, 2000)


    def run(self, ):
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for ent in self.entity_list:
                if isinstance(ent, list):
                    for sub_ent in ent:
                        self.window.blit(source=sub_ent.surf, dest=sub_ent.rect)
                        sub_ent.move()
                else:
                    self.window.blit(source=ent.surf, dest=ent.rect)
                    ent.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.jump()
                if event.type == EVENT_OBSTACLE:
                    choice = random.choice(('Obstacle1Img0','Obstacle1Img0'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            for obs in self.obstacle2_images:
                obs.rect.x -= 5
                if obs.rect.left <= 0:
                    obs.rect.x = WIN_WIDTH

            self.player.updateJump()
            self.player.move()

            # Update the player animation index
            self.animation_counter += 3
            if self.animation_counter > 25:
                self.animation_counter = 0
                self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

            # Updade the obstacle animation
            self.obstacle2_animation_counter += 3
            if self.obstacle2_animation_counter > 25:
                self.obstacle2_animation_counter = 0
                self.current_obstacle2_image_index = (self.current_player_image_index + 1) % len(self.obstacle2_images)

            current_player = self.player_images[self.current_player_image_index]
            current_player.rect.topleft = self.player.rect.topleft
            self.window.blit(current_player.image, current_player.rect.topleft)

            current_obstacle2 = self.obstacle2_images[self.current_obstacle2_image_index]
            current_obstacle2.rect.topleft = obs.rect.topleft
            self.window.blit(current_obstacle2.image, current_obstacle2.rect.topleft)
            pygame.display.flip()

            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000: .1f}s', C_PURPLE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps() :0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()
            EntityMediator.verify_collision(entity_list=self.entity_list)

            pass

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
