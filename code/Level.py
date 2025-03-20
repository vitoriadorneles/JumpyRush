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
            window (Surface): The Pygame window surface for rendering.
            name (str): The level name (e.g., Level1).
            score_manager (Score): The Score class instance for managing scores.
        """
        self.window = window
        self.name = name
        self.score_manager = score_manager  # Instance of Score for managing score persistence

        # Initialize entities and player
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))  # Load background entities
        self.player_images = EntityFactory.get_entity("PlayerImg")  # Load player images
        self.player = Player("PlayerImg0", (25, WIN_HEIGHT - 130))  # Initialize the player
        self.entity_list.append(self.player)

        # Animation and obstacle properties
        self.current_player_image_index = 0
        self.animation_counter = 0
        pygame.time.set_timer(EVENT_OBSTACLE, 3000)

        # Score and time tracking
        self.score = 0
        self.game_time = 0
        self.score_update_counter = 0

    def run(self):
        """Main game loop for the level."""
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')  # Load background music
        pygame.mixer_music.play(-1)  # Loop background music
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)  # Cap FPS to 60
            self.window.fill((0, 0, 0))  # Clear the screen

            # Game updates
            self.update_score_and_time()
            self.update_entities()
            self.update_player_animation()

            # Event processing
            if self.process_events() == "exit":
                return "game_over"

            # Render HUD
            self.render_hud(clock)

            pygame.display.flip()  # Update the display

    def update_score_and_time(self):
        """Update the player's score and game time dynamically."""
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
        """Update the movement and rendering of all entities."""
        for entity in self.entity_list:
            self.window.blit(entity.surf, entity.rect)  # Draw entity
            entity.move()  # Update entity position

    def update_player_animation(self):
        """Animate the player's movement and synchronize its position."""
        self.player.updateJump()  # Update jump state
        self.animation_counter += 1
        if self.animation_counter > 25:
            self.animation_counter = 0
            self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

        current_image = self.player_images[self.current_player_image_index]
        current_image.rect.topleft = self.player.rect.topleft  # Sync player position with animation
        self.window.blit(current_image.image, current_image.rect)

    def process_events(self):
        """Process all events such as user input and obstacle generation."""
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
            return "exit"

    def generate_obstacle(self):
        """Generate a new obstacle and add it to the entity list."""
        obstacle_choice = random.choice(('Obstacle1Img0', 'Obstacle1Img1'))
        obstacle_speed = 5 + (self.score // 10)
        new_obstacle = EntityFactory.get_entity(obstacle_choice, speed=obstacle_speed)
        self.entity_list.append(new_obstacle)

    def render_hud(self, clock):
        """Render the heads-up display (HUD)."""
        self.render_text(14, f'{self.name} - Time: {self.game_time:.1f}s', C_PURPLE, (10, 5))
        self.render_text(14, f'Score: {self.score}', C_PURPLE, (WIN_WIDTH - 120, 5))
        self.render_text(14, f'FPS: {clock.get_fps():.0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
        self.render_text(14, f'Entities: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))

    def render_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        """Render and display text on the screen."""
        font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surface = font.render(text, True, text_color).convert_alpha()
        text_rect = text_surface.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surface, text_rect)

    def show_game_over(self):
        """Display the Game Over screen and save the player's score."""
        self.window.fill((0, 0, 0))  # Clear the screen

        # Render "Game Over" message
        font = pygame.font.Font("./assets/LevelFont.ttf", 50)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
        self.window.blit(game_over_text, game_over_rect)

        # Render final score and game time
        score_font = pygame.font.Font("./assets/LevelFont.ttf", 30)
        score_text = score_font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.window.blit(score_text, score_rect)

        time_text = score_font.render(f"Game Time: {self.game_time:.1f}s", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))
        self.window.blit(time_text, time_rect)

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait before returning to the menu

        # Save the player's score using Score class
        self.score_manager.save_score(self.score, self.game_time)
