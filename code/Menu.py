import pygame
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import WIN_WIDTH, WIN_HEIGHT, C_PURPLE, C_WHITE, C_BLACK, MENU_OPTION
from code.Score import Score  # Import the Score class


class Menu:
    def __init__(self, window):
        """Initialize the menu and its necessary resources."""
        self.window = window
        self.surf = pygame.image.load('./assets/MenuBg.png').convert_alpha()  # Load the background image
        self.rect = self.surf.get_rect(left=0, top=0)  # Position the background
        self.score_manager = Score()  # Instantiate the Score manager for handling scores

    def run(self):
        """Run the menu loop, allowing users to navigate and select options."""
        menu_option = 0
        # Load and play menu background music
        pygame.mixer_music.load('./assets/Menu.mp3')
        pygame.mixer_music.play(-1)

        while True:
            # Render the menu background and title
            self.window.blit(source=self.surf, dest=self.rect)
            self.render_text(50, 'Jumpy', C_PURPLE, ((WIN_WIDTH / 2), 70))
            self.render_text(50, 'Rush', C_PURPLE, ((WIN_WIDTH / 2), 120))

            # Render menu options dynamically
            for i in range(len(MENU_OPTION)):
                color = C_WHITE if i == menu_option else C_BLACK
                self.render_text(20, MENU_OPTION[i], color, ((WIN_WIDTH / 2), 190 + 30 * i))

            pygame.display.flip()  # Refresh the screen

            # Handle user input for navigation and selection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)  # Move to next option
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)  # Move to previous option
                    elif event.key == pygame.K_RETURN:
                        # Handle user selection
                        if MENU_OPTION[menu_option] == "SCORE":
                            self.show_scores()  # Display the scores
                        else:
                            return MENU_OPTION[menu_option]  # Return selected option to the caller

    def render_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        """Render and display text on the menu."""
        font: Font = pygame.font.Font("./assets/MenuFont.ttf", text_size)
        text_surf: Surface = font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

    def save_score(self, score, game_time):
        try:
            with open(self.scores_file, 'a') as file:
                file.write(f'{score},{game_time:.1f}\n')  # Salva score e tempo no formato CSV
            print(f"Score salvo com sucesso: {score}, tempo: {game_time:.1f}s")
        except Exception as e:
            print(f"Erro ao salvar o score: {e}")

    def show_scores(self):
        """Display the last three scores fetched from the Score class."""
        scores = self.score_manager.load_scores(limit=3)  # Fetch the latest 3 scores from the database

        # Clear the screen and render the score header
        self.window.fill((0, 0, 0))
        self.render_text(50, "Last Scores", C_PURPLE, ((WIN_WIDTH / 2), 50))

        # Render scores or fallback message if no scores exist
        if scores:
            for i, (score, game_time) in enumerate(scores):
                score_text = f"{i + 1}. Score: {score} - Time: {game_time:.1f}s"
                self.render_text(30, score_text, C_WHITE, ((WIN_WIDTH / 2), 150 + 40 * i))
        else:
            self.render_text(30, "No scores available.", C_WHITE, ((WIN_WIDTH / 2), WIN_HEIGHT / 2))

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait 3 seconds before returning to the menu
