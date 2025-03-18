import sys
import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Menu import Menu
from code.Level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Jumpy Rush")

    def show_main_menu(self):
        menu = Menu(self.window)
        menu.run()

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:  # Iniciar jogo
                level = Level(self.window, 'Level1', self)
                level_result = level.run()  # Executa o jogo
                if level_result == "game_over":
                    continue  # Volta ao menu principal após Game Over

            elif menu_return == MENU_OPTION[2]:  # Sair
                pygame.quit()
                quit()
