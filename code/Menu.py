import os

import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, C_PURPLE, MENU_OPTION, C_WHITE, C_BLACK, WIN_HEIGHT


class Menu:
    def __init__(self, window):
        self.score = []
        self.game_time = []
        self.window = window
        # Carregar a imagem de fundo
        self.surf = pygame.image.load('./assets/MenuBg.png').convert_alpha()
        self.scores_file = os.path.join(os.path.dirname(__file__), 'scores.txt')
        # Criar o retângulo para posicionar a imagem
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        # Carregar música
        pygame.mixer_music.load('./assets/Menu.mp3')
        # Tocar música
        pygame.mixer_music.play(-1)

        while True:
            # Desenhar o plano de fundo
            self.window.blit(source=self.surf, dest=self.rect)

            self.menu_text(50, 'Jumpy', C_PURPLE, ((WIN_WIDTH / 2), 70))
            self.menu_text(50, 'Rush', C_PURPLE, ((WIN_WIDTH / 2), 120))

            # Desenhar opções do menu
            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), 190 + 30 * i))
                else:
                    self.menu_text(20, MENU_OPTION[i], C_BLACK, ((WIN_WIDTH / 2), 190 + 30 * i))

            # Atualizar a tela
            pygame.display.flip()

            # Verificar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()  # Encerra o Pygame

                # Verificar tecla pressionada
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
                        if MENU_OPTION[menu_option] == "SCORE":  # Verifica se a opção é "Score"
                            print("Opção Score selecionada.")  # Depuração
                            self.show_scores()  # Exibe os scores
                            continue  # Volta ao menu após exibir os scores
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/MenuFont.ttf", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

    def show_scores(self):
        """Exibe os últimos três scores registrados na tela."""
        scores = self.load_scores()  # Carrega os scores do arquivo

        self.window.fill((0, 0, 0))  # Limpa a tela com preto
        self.menu_text(50, "Últimos Scores", C_PURPLE, ((WIN_WIDTH / 2), 50))

        if scores:
            for i, (score, time_played) in enumerate(scores):
                score_text = f"{i + 1}. Score: {score} - Tempo: {time_played:.1f}s"
                self.menu_text(30, score_text, C_WHITE, ((WIN_WIDTH / 2), 150 + 40 * i))
        else:
            self.menu_text(30, "Nenhum score disponível.", C_WHITE, ((WIN_WIDTH / 2), WIN_HEIGHT / 2))

        pygame.display.flip()
        pygame.time.wait(3000)  # Aguarda 3 segundos antes de retornar ao menu
        return  # Retorna ao menu principal

    def save_score(self, score, game_time):
        try:
            with open(self.scores_file, 'a') as file:
                file.write(f'{score},{game_time:.1f}\n')  # Salva score e tempo no formato CSV
            print(f"Score salvo com sucesso: {score}, tempo: {game_time:.1f}s")
        except Exception as e:
            print(f"Erro ao salvar o score: {e}")

    def load_scores(self):
        scores = []
        try:
            with open(self.scores_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    score, time_played = line.strip().split(',')
                    scores.append((int(score), float(time_played)))

                print(f"[DEBUG] Scores carregados: {scores}")
                return scores[-3:] if len(scores) > 3 else scores
        except FileNotFoundError:
            print("[DEBUG] Arquivo de scores não encontrado. Nenhum score disponível.")
            return []  # Retorna lista vazia se o arquivo não existir
        except Exception as e:
            print(f"Erro ao carregar scores: {e}")
            return []

