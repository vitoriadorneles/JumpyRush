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
        self.EVENT_OBSTACLE = None
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

        pygame.time.set_timer(EVENT_OBSTACLE, 3000)

    def run(self):
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)  # Limitando para 60 FPS
            self.window.fill((0, 0, 0))  # Limpa a tela antes de redesenhar

            # Atualizando e desenhando as entidades de fundo e player
            for ent in self.entity_list:
                if isinstance(ent, list):
                    for sub_ent in ent:
                        self.window.blit(source=sub_ent.surf, dest=sub_ent.rect)
                        sub_ent.move()
                else:
                    self.window.blit(source=ent.surf, dest=ent.rect)
                    ent.move()

            # Eventos de entrada
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.jump()
                        jump_sound = pygame.mixer.Sound('./assets/JumpSong.mp3')
                        jump_sound.play()

                if event.type == EVENT_OBSTACLE:
                    choice = random.choice(('Obstacle1Img0', 'Obstacle1Img1'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            # Atualizando e desenhando o player
            self.player.updateJump()
            self.player.move()
            self.animation_counter += 1
            if self.animation_counter > 25:
                self.animation_counter = 0
                self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

            current_player = self.player_images[self.current_player_image_index]
            current_player.rect.topleft = self.player.rect.topleft
            self.window.blit(current_player.image, current_player.rect)

            for obs in self.obstacle2_images:
                obs.rect.x -= 6
                if obs.rect.left <= 0:
                    obs.rect.x = WIN_WIDTH

            self.obstacle2_animation_counter += 5
            if self.obstacle2_animation_counter > 25:  # Ajuste o valor para controlar a velocidade da animação
                self.obstacle2_animation_counter = 0
                self.current_obstacle2_image_index = (self.current_obstacle2_image_index + 1) % len(
                    self.obstacle2_images)

            # Atualizando a imagem atual do obstáculo
            current_obstacle2 = self.obstacle2_images[self.current_obstacle2_image_index]
            self.window.blit(current_obstacle2.image, current_obstacle2.rect)  # Renderizando o obstáculo

            # HUD de informações do jogo
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000: .1f}s', C_PURPLE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))

            # Verificando colisões e integridade das entidades
            if EntityMediator.check_collision(self.player, self.entity_list):
                self.player.health -= 10  # Reduz a saúde do jogador
                if self.player.health <= 0:
                    print("Game Over!")

            # Atualização da tela
            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)