import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, C_PURPLE, MENU_OPTION, C_WHITE, C_BLACK


class Menu:
    def __init__(self, window):
        self.window = window
        # upload the image
        self.surf = pygame.image.load('./assets/MenuBg.png')
        # Creating a rectangle to place the image
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        # Loading music
        pygame.mixer_music.load('./assets/Menu.mp3')
        # Playing music
        pygame.mixer_music.play(-1)

        while True:
            # Sending the image to the rectangle
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, 'Jumpy', C_PURPLE, ((WIN_WIDTH / 2), 70))
            self.menu_text(50, 'Rush', C_PURPLE, ((WIN_WIDTH / 2), 120))

            for i in range(len(MENU_OPTION)):
                self.menu_text(20, MENU_OPTION[i], C_BLACK, ((WIN_WIDTH / 2), 170 + 25 * i))

            # Updating the screen
            pygame.display.flip()

            # Checking all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # close window
                    quit()  # emd pygame

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
