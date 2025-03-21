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
            score_manager (Score): Score manager instance for saving game scores.
        """
        self.window = window
        self.name = name
        self.score_manager = score_manager  # Reference to Score manager

        # Initialize entities
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))  # Background entities
        self.player_images = EntityFactory.get_entity("PlayerImg")  # Player sprites
        self.player = Player("PlayerImg0", (25, WIN_HEIGHT - 130))  # Initialize Player entity
        self.entity_list.append(self.player)

        # Animation settings
        self.current_player_image_index = 0
        self.animation_counter = 0
        pygame.time.set_timer(EVENT_OBSTACLE, 3000)

        # Score tracking
        self.score = 0
        self.game_time = 0
        self.score_update_counter = 0

    def run(self):
        """Main game loop."""
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')  # Background music
        pygame.mixer_music.play(-1)  # Play on loop
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)  # Cap FPS at 60
            self.window.fill((0, 0, 0))  # Clear screen

            # Handle game updates
            self.update_score_and_time()
            self.update_entities()
            self.update_player_animation()

            # Process events
            if self.process_events() == "game_over":
                return "game_over"

            # Render HUD
            self.render_hud(clock)

            pygame.display.flip()  # Update display

    def update_score_and_time(self):
        """Update player's score and game time dynamically."""
        self.score_update_counter += 1
        if self.score_update_counter >= 30:  # Update every half-second (~30 frames)
            self.score += 2
            self.game_time += 0.5
            self.score_update_counter = 0

            # Increase obstacle speed dynamically based on score
            if self.score % 10 == 0:
                for entity in self.entity_list:
                    if isinstance(entity, Obstacle):
                        entity.speed += 1

    def update_entities(self):
        """Update movement and render all entities."""
        for entity in self.entity_list:
            self.window.blit(entity.surf, entity.rect)  # Render entity
            entity.move()  # Update position

    def update_player_animation(self):
        """Animate player's movement."""
        self.player.updateJump()
        self.animation_counter += 1
        if self.animation_counter > 25:  # Update animation every 25 frames
            self.animation_counter = 0
            self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

        current_image = self.player_images[self.current_player_image_index]
        current_image.rect.topleft = self.player.rect.topleft  # Sync player position with animation
        self.window.blit(current_image.image, current_image.rect)

    def process_events(self):
        """Handle all events, including player input and obstacle generation."""
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

        # Check for collisions
        if EntityMediator.verify_collision(self.entity_list) == "game_over":
            self.show_game_over()
            return "game_over"

    def generate_obstacle(self):
        """Generate and add a new obstacle to the entity list."""
        obstacle_choice = random.choice(('Obstacle1Img0', 'Obstacle1Img1'))
        obstacle_speed = 5 + (self.score // 10)  # Increase speed based on score
        new_obstacle = EntityFactory.get_entity(obstacle_choice, speed=obstacle_speed)
        self.entity_list.append(new_obstacle)

    def render_hud(self, clock):
        """Render heads-up display (HUD)."""
        self.render_text(14, f'{self.name} - Time: {self.game_time:.1f}s', C_PURPLE, (10, 5))
        self.render_text(14, f'Score: {self.score}', C_PURPLE, (WIN_WIDTH - 120, 5))
        self.render_text(14, f'FPS: {clock.get_fps():.0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
        self.render_text(14, f'Entities: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))

    def render_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        """Render text on the screen."""
        font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surface = font.render(text, True, text_color).convert_alpha()
        text_rect = text_surface.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surface, text_rect)

    def show_game_over(self):
        """Display Game Over screen and save player's score."""
        self.window.fill((0, 0, 0))  # Clear screen

        # Display Game Over message
        font = pygame.font.Font("./assets/LevelFont.ttf", 50)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
        self.window.blit(game_over_text, game_over_rect)

        # Display final score and game time
        score_font = pygame.font.Font("./assets/LevelFont.ttf", 30)
        score_text = score_font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.window.blit(score_text, score_rect)

        time_text = score_font.render(f"Game Time: {self.game_time:.1f}s", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))
        self.window.blit(time_text, time_rect)

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait before returning to the menu

        # Save player's score using Score manager
        self.score_manager.save_score(self.score, self.game_time)
