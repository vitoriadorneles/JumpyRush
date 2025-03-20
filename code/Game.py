import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Menu import Menu
from code.Level import Level


class Game:
    def __init__(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Jumpy Rush")

    def show_main_menu(self):
        # Display the main menu
        menu = Menu(self.window)
        menu.run()

    def run(self):
        # Main game loop
        while True:
            menu = Menu(self.window)  # Create the menu instance
            menu_return = menu.run()  # Run the menu and get the selected option

            if menu_return == MENU_OPTION[0]:  # Start game option
                level = Level(self.window, 'Level1', menu)  # Pass the menu instance to the Level
                level_result = level.run()  # Run the level loop
                if level_result == "game_over":
                    continue  # Return to the main menu after Game Over

            elif menu_return == MENU_OPTION[2]:  # Quit option
                pygame.quit()
                quit()  # Exit the game
