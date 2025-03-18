import random
import sys
import pygame
from pygame import KEYDOWN, K_SPACE
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

        pygame.time.set_timer(EVENT_OBSTACLE, 3000)
        self.entity_list.append(self.player)

    def run(self):
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.window.fill((0, 0, 0))

            # Atualizando entidades
            for ent in self.entity_list:
                if isinstance(ent, list):
                    for sub_ent in ent:
                        self.window.blit(source=sub_ent.surf, dest=sub_ent.rect)
                        sub_ent.move()
                else:
                    self.window.blit(source=ent.surf, dest=ent.rect)
                    ent.move()

            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.player.jump()
                    jump_sound = pygame.mixer.Sound('./assets/JumpSong.mp3')
                    jump_sound.play()
                if event.type == EVENT_OBSTACLE:
                    choice = random.choice(('Obstacle1Img0', 'Obstacle1Img1'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            # Atualizar o player
            self.player.updateJump()
            self.animation_counter += 1
            if self.animation_counter > 25:
                self.animation_counter = 0
                self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

            current_player = self.player_images[self.current_player_image_index]
            current_player.rect.topleft = self.player.rect.topleft
            self.window.blit(current_player.image, current_player.rect)

            # Informações de HUD
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000: .1f}s', C_PURPLE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))

            # Verificar colisões
            collision_result = EntityMediator.verify_collision(entity_list=self.entity_list)
            if collision_result == "game_over":
                return "game_over"

            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surf = font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

    def show_game_over(self):
        self.window.fill((0, 0, 0))

        font = pygame.font.Font("./assets/LevelFont.ttf", 50)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.window.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.wait(3000)
        return "game_over"
