import os
import sqlite3
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import WIN_WIDTH, WIN_HEIGHT, C_PURPLE, C_WHITE, C_BLACK, MENU_OPTION


class Menu:
    def __init__(self, window):
        """Initialize the menu with the game window and database setup."""
        self.window = window
        self.db_file = os.path.join(os.path.dirname(__file__), 'scores.db')  # Path to the SQLite database
        self.surf = pygame.image.load('./assets/MenuBg.png').convert_alpha()  # Load the menu background image
        self.rect = self.surf.get_rect(left=0, top=0)  # Position the background image

        # Create the database table for scores if it does not exist
        self.create_table()

    def create_table(self):
        """Create the 'scores' table in the SQLite database if it doesn't exist."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                game_time REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def run(self):
        """Run the menu loop to display options and handle user interaction."""
        menu_option = 0  # Tracks the currently selected menu option
        # Load and play the menu background music
        pygame.mixer_music.load('./assets/Menu.mp3')
        pygame.mixer_music.play(-1)

        while True:
            # Render the menu background and title
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, 'Jumpy', C_PURPLE, ((WIN_WIDTH / 2), 70))
            self.menu_text(50, 'Rush', C_PURPLE, ((WIN_WIDTH / 2), 120))

            # Display the menu options
            for i in range(len(MENU_OPTION)):
                color = C_WHITE if i == menu_option else C_BLACK
                self.menu_text(20, MENU_OPTION[i], color, ((WIN_WIDTH / 2), 190 + 30 * i))

            pygame.display.flip()  # Update the screen

            # Handle user input for navigation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)  # Move down the options
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)  # Move up the options
                    elif event.key == pygame.K_RETURN:
                        # Handle the selected option
                        if MENU_OPTION[menu_option] == "SCORE":
                            self.show_scores()  # Display the score screen
                            continue
                        return MENU_OPTION[menu_option]  # Return the selected option to the caller

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        """Render and display text on the menu screen."""
        font: Font = pygame.font.Font("./assets/MenuFont.ttf", text_size)  # Load the font
        text_surf: Surface = font.render(text, True, text_color).convert_alpha()  # Render the text
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)  # Center the text
        self.window.blit(source=text_surf, dest=text_rect)  # Draw the text to the screen

    def save_score(self, score, game_time):
        """Save a new score and game time into the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO scores (score, game_time) VALUES (?, ?)', (score, game_time))
            conn.commit()
            conn.close()
            print(f"[DEBUG] Score saved to the database: {score}, time: {game_time:.1f}s")
        except Exception as e:
            print(f"Error saving score: {e}")

    def load_scores(self):
        """Load the last 3 scores from the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT score, game_time FROM scores ORDER BY id DESC LIMIT 3')
            scores = cursor.fetchall()
            conn.close()
            print(f"[DEBUG] Scores loaded from the database: {scores}")
            return scores
        except Exception as e:
            print(f"Error loading scores: {e}")
            return []

    def show_scores(self):
        """Display the last three scores on the screen."""
        scores = self.load_scores()  # Fetch scores from the database

        # Clear the screen
        self.window.fill((0, 0, 0))
        self.menu_text(50, "Last Scores", C_PURPLE, ((WIN_WIDTH / 2), 50))

        if scores:
            # Display each score
            for i, (score, game_time) in enumerate(scores):
                score_text = f"{i + 1}. Score: {score} - Time: {game_time:.1f}s"
                self.menu_text(30, score_text, C_WHITE, ((WIN_WIDTH / 2), 150 + 40 * i))
        else:
            # Display message if no scores are available
            self.menu_text(30, "No scores available.", C_WHITE, ((WIN_WIDTH / 2), WIN_HEIGHT / 2))

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait before returning to the menu
