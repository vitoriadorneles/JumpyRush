import pygame

pygame.init()

print('Setup Start')
# criando janela
window = pygame.display.set_mode(size=(800, 480))
print('Setup End')

print('Loop Start')
# loop para janela permanecer aberta e depois fechar com o quit
while True:
    # verificando todos os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # close window
            quit()  # emd pygame
