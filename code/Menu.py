import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, C_PURPLE, MENU_OPTION, C_WHITE, C_BLACK, BTN_SIZE


class Menu:
    def __init__(self, window):
        self.window = window
        # upload the image
        self.surf = pygame.image.load('./assets/MenuBg.png').convert_alpha()
        # Creating a rectangle to place the image
        self.rect = self.surf.get_rect(left=0, top=0)

        # upload button images
        self.btn_unpressed = pygame.transform.scale(pygame.image.load('./assets/Button_unpressed.png'), BTN_SIZE)
        self.btn_pressed = pygame.transform.scale(pygame.image.load('./assets/Button_pressed.png'), BTN_SIZE)

        self.btn_rect = self.btn_unpressed.get_rect(center=(WIN_WIDTH / 2, 190))

    def run(self):
        menu_option = 0
        # Loading music
        pygame.mixer_music.load('./assets/Menu.mp3')
        # Playing music
        pygame.mixer_music.play(-1)

        while True:
            # Draw background
            self.window.blit(source=self.surf, dest=self.rect)

            self.menu_text(50, 'Jumpy', C_PURPLE, ((WIN_WIDTH / 2), 70))
            self.menu_text(50, 'Rush', C_PURPLE, ((WIN_WIDTH / 2), 120))

            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]  # Check if the left button has been pressed

            options_rects = []

            # Draw menu options and store their rects
            start_y = self.btn_rect.bottom + 20
            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), 190 + 30 * i))
                else:
                    self.menu_text(20, MENU_OPTION[i], C_BLACK, ((WIN_WIDTH / 2), 190 + 30 * i))

            # Updating the screen
            pygame.display.flip()

            # Checking all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # close window
                    quit()  # emd pygame

                # Check if the mouse is over the button
                if self.btn_rect.collidepoint(mouse_pos):
                    new_game_color = C_WHITE
                    btn_image = self.btn_pressed if mouse_clicked else self.btn_unpressed
                else:
                    new_game_color = C_BLACK
                    btn_image = self.btn_unpressed

                # Check the Key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/MenuFont.ttf", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
