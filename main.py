import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configura a tela cheia
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("BLCKSHRN")

# Define a cor do texto e a fonte
text_color = (255, 255, 255)  # Branco
font = pygame.font.Font(None, 120)  # Define o tamanho da fonte

# Renderiza o texto
text = font.render("BLCKSHRN", True, text_color)
text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Preenche a tela com uma cor de fundo
    screen.fill((0, 0, 0))  # Preto

    # Exibe o texto no centro da tela
    screen.blit(text, text_rect)

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()