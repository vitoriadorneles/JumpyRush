import random
import sys
import pygame
from pygame import KEYDOWN, K_SPACE
from code.Const import C_PURPLE, WIN_HEIGHT, WIN_WIDTH, EVENT_OBSTACLE
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Obstacle import Obstacle
from code.Player import Player


class Level:
    def __init__(self, window, name, score_manager):
        """
        Initialize the level settings.

        Args:
            window (Surface): Pygame window surface for rendering.
            name (str): Level name (e.g., 'Level1').
            score_manager (Score): Score manager instance for saving and loading scores.
        """
        self.window = window
        self.name = name
        self.score_manager = score_manager

        # Initialize entities and player
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.player_images = EntityFactory.get_entity("PlayerImg")
        self.player = Player("PlayerImg0", (25, WIN_HEIGHT - 130))
        self.entity_list.append(self.player)

        # Animation and score tracking
        self.current_player_image_index = 0
        self.animation_counter = 0
        pygame.time.set_timer(EVENT_OBSTACLE, 3000)
        self.score = 0
        self.game_time = 0
        self.score_update_counter = 0

    def run(self):
        """Main game loop for the level."""
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.window.fill((0, 0, 0))

            # Update game mechanics
            self.update_score_and_time()
            self.update_entities()
            self.update_player_animation()

            # Handle events and process user input
            if self.process_events() == "exit":
                return "game_over"

            # Render HUD
            self.render_hud(clock)

            pygame.display.flip()

    def update_score_and_time(self):
        """Update the score and game time dynamically."""
        self.score_update_counter += 1
        if self.score_update_counter >= 30:  # Every 0.5 seconds
            self.score += 2
            self.game_time += 0.5
            self.score_update_counter = 0

            if self.score % 10 == 0:  # Every 10 points, increase obstacle speed
                for entity in self.entity_list:
                    if isinstance(entity, Obstacle):
                        entity.speed += 1

    def update_entities(self):
        """Update the movement and rendering of entities."""
        for entity in self.entity_list:
            self.window.blit(entity.surf, entity.rect)
            entity.move()

    def update_player_animation(self):
        """Update player animation and synchronize with position."""
        self.player.updateJump()
        self.animation_counter += 1
        if self.animation_counter > 25:
            self.animation_counter = 0
            self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

        current_image = self.player_images[self.current_player_image_index]
        current_image.rect.topleft = self.player.rect.topleft
        self.window.blit(current_image.image, current_image.rect)

    def process_events(self):
        """Handle player input and game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.player.jump()
                jump_sound = pygame.mixer.Sound('./assets/JumpSong.mp3')
                jump_sound.play()
            if event.type == EVENT_OBSTACLE:
                self.generate_obstacle()

        if EntityMediator.verify_collision(self.entity_list) == "game_over":
            self.show_game_over()
            return "exit"

    def generate_obstacle(self):
        """Generate a new obstacle."""
        obstacle_choice = random.choice(('Obstacle1Img0', 'Obstacle1Img1'))
        obstacle_speed = 5 + (self.score // 10)
        new_obstacle = EntityFactory.get_entity(obstacle_choice, speed=obstacle_speed)
        self.entity_list.append(new_obstacle)

    def render_hud(self, clock):
        """Render heads-up display (HUD)."""
        self.render_text(14, f'{self.name} - Time: {self.game_time:.1f}s', C_PURPLE, (10, 5))
        self.render_text(14, f'Score: {self.score}', C_PURPLE, (WIN_WIDTH - 120, 5))
        self.render_text(14, f'FPS: {clock.get_fps():.0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
        self.render_text(14, f'Entities: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))

    def render_text(self, text_size, text, color, position):
        """Render text."""
        font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surface = font.render(text, True, color).convert_alpha()
        text_rect = text_surface.get_rect(left=position[0], top=position[1])
        self.window.blit(text_surface, text_rect)

    def show_game_over(self):
        """Display the Game Over screen and save the player's score."""
        self.window.fill((0, 0, 0))
        font = pygame.font.Font("./assets/LevelFont.ttf", 50)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        self.window.blit(game_over_text, game_over_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50)))

        score_font = pygame.font.Font("./assets/LevelFont.ttf", 30)
        self.window.blit(score_font.render(f"Your Score: {self.score}", True, (255, 255, 255)),
                         score_font.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))
        self.window.blit(score_font.render(f"Game Time: {self.game_time:.1f}s", True, (255, 255, 255)),
                         score_font.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))

        pygame.display.flip()
        pygame.time.wait(3000)
        self.score_manager.save_score(self.score, self.game_time)


