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
    def __init__(self, window, name, menu_instance):
        # Initialize level settings
        self.window = window
        self.name = name
        self.menu_instance = menu_instance  # Instance of Menu for saving scores
        self.entity_list: list[Entity] = []  # List to store game entities
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))  # Load background entities
        self.game_time = 0  # Total game time in seconds

        # Player configuration
        self.player_images = EntityFactory.get_entity("PlayerImg")  # Load player images for animation
        self.player = Player("PlayerImg0", (25, WIN_HEIGHT - 130))  # Initialize player position
        self.current_player_image_index = 0  # Index for player image animation
        self.animation_counter = 0  # Counter for animation timing

        # Score configuration
        self.score = 0  # Initialize score
        self.score_update_counter = 0  # Counter for managing score increments

        # Timer to generate obstacles periodically
        pygame.time.set_timer(EVENT_OBSTACLE, 3000)
        self.entity_list.append(self.player)

    def run(self):
        """Main loop for the level gameplay."""
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')  # Load background music
        pygame.mixer_music.play(-1)  # Play background music on loop
        clock = pygame.time.Clock()  # Create a clock to manage frame rates

        while True:
            clock.tick(60)  # Limit FPS to 60
            self.window.fill((0, 0, 0))  # Clear the screen

            # Increment score and game time
            self.score_update_counter += 1
            if self.score_update_counter >= 30:  # Update every half-second (~30 frames)
                self.score += 2  # Increase score
                self.game_time += 0.5  # Increase game time
                self.score_update_counter = 0

                # Increase obstacle speed based on score
                if self.score % 10 == 0:  # Every 10 points
                    for entity in self.entity_list:
                        if isinstance(entity, Obstacle):
                            entity.speed += 1  # Increase obstacle speed

            # Update and render entities
            for ent in self.entity_list:
                self.window.blit(ent.surf, ent.rect)  # Draw entity on screen
                ent.move()  # Update entity movement

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.player.jump()  # Trigger player jump
                    jump_sound = pygame.mixer.Sound('./assets/JumpSong.mp3')  # Load jump sound
                    jump_sound.play()  # Play jump sound

                if event.type == EVENT_OBSTACLE:  # Generate new obstacle
                    choice = random.choice(('Obstacle1Img0', 'Obstacle1Img1'))
                    current_speed = 5 + (self.score // 10)  # Speed increases with score
                    new_obstacle = EntityFactory.get_entity(choice, speed=current_speed)  # Create obstacle
                    self.entity_list.append(new_obstacle)

            # Update player animation
            self.player.updateJump()
            self.animation_counter += 1
            if self.animation_counter > 25:
                self.animation_counter = 0
                self.current_player_image_index = (self.current_player_image_index + 1) % len(self.player_images)

            current_player = self.player_images[self.current_player_image_index]
            current_player.rect.topleft = self.player.rect.topleft  # Synchronize player position with animation
            self.window.blit(current_player.image, current_player.rect)

            # Display HUD information
            self.level_text(14, f'{self.name} - Time: {self.game_time:.1f}s', C_PURPLE, (10, 5))
            self.level_text(14, f'Score: {self.score}', C_PURPLE, (WIN_WIDTH - 120, 5))
            self.level_text(14, f'FPS: {clock.get_fps():.0f}', C_PURPLE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'Entities: {len(self.entity_list)}', C_PURPLE, (10, WIN_HEIGHT - 20))

            # Check for collisions
            collision_result = EntityMediator.verify_collision(entity_list=self.entity_list)
            if collision_result == "game_over":
                self.show_game_over()
                return "game_over"

            pygame.display.flip()  # Update the screen

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        """Display text on the HUD."""
        font = pygame.font.Font("./assets/LevelFont.ttf", text_size)
        text_surf = font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

    def show_game_over(self):
        """Display the Game Over screen and save the score."""
        self.window.fill((0, 0, 0))  # Clear the screen with black

        # Display Game Over message
        font = pygame.font.Font("./assets/LevelFont.ttf", 50)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
        self.window.blit(text, text_rect)

        # Display final score
        score_font = pygame.font.Font("./assets/LevelFont.ttf", 30)
        score_text = score_font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.window.blit(score_text, score_text_rect)

        # Display total game time
        time_text = score_font.render(f"Game Time: {self.game_time:.1f}s", True, (255, 255, 255))
        time_text_rect = time_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))
        self.window.blit(time_text, time_text_rect)

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait before returning to the menu

        # Save score in the database using menu_instance
        self.menu_instance.save_score(self.score, self.game_time)
