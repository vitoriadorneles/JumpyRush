import pygame

from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        # criando janela
        self.window = pygame.display.set_mode(size=(800, 480))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass

            # verificando todos os eventos
            # for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        pygame.quit()  # close window
            #        quit()  # emd pygame
