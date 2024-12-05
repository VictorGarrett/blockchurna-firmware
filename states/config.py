import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("BLCKSHRN")
clock = pygame.time.Clock()
pygame.mixer.init()

pirilim_candidate = pygame.mixer.Sound("./assets/inter.mp3")
pirilim_end = pygame.mixer.Sound("./assets/fim.mp3")

text_color = (255, 255, 255)
font = pygame.font.Font(None, 120)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (214, 226, 255)  # Light blue for the bottom bar
GREEN = (0, 150, 0)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
font_very_large = pygame.font.Font(None, 82)
font_extra_large = pygame.font.Font(None, 112)

# Helper functions
def render_multiline_text(text, font, color, start_pos, line_spacing):
    """Helper function to render multiline text."""
    lines = text.splitlines()
    y = start_pos[1]
    for line in lines:
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (start_pos[0], y))
        y += line_surface.get_height() + line_spacing