import sys

import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu

pygame.display.set_caption("Jumpy Rush")


class Game:
    def __init__(self):
        pygame.init()
        # criando janela
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def show_main_menu(self):
        menu = Menu(self.window)
        menu.run()

    def run(self):
        # window open
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:  # Iniciar jogo
                level = Level(self.window, 'Level1', self)
                level_result = level.run()  # Espera a execução do jogo
                if level_result == "game_over":
                    continue  # Volta para o menu sem erro

            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pass
