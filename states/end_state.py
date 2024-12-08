from states.state import State
import states.config as config
from datetime import datetime
import sys
import pygame
from threading import Timer
from text_to_speech.text_to_speech import text_to_speech

class EndState(State):
    def __init__(self):
        super().__init__()
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))

        self.title_text = "FIM"
        self.instruction_text = "Retire seu comprovante"
        self.footer_text = "Município - Zona - Seção"
        self.first_render = True
        
    def reset_state(self):
        self.next_state = "Identification"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next_state = "Identification"

    def render(self, screen):
        if self.first_render:
            config.pirilim_end.play()
            r = Timer(5.0, self.reset_state)
            r.start()
            text_to_speech(f"Fim, retire seu comprovante.")
            self.first_render = False
        screen.fill(config.WHITE)

        # Render date and time
        datetime_text = datetime.now().strftime("%Y-%m-%d\n%H:%M:%S")
        config.render_multiline_text(datetime_text, config.font_small, config.BLACK, (20, 20), line_spacing=5)


        # Render main title
        title_surface = config.font_extra_large.render(self.title_text, True, config.BLACK)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60))
        screen.blit(title_surface, title_rect)

        # Render instructions
        instruction_surface = config.font_large.render(self.instruction_text, True, config.BLACK)
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 ))
        screen.blit(instruction_surface, instruction_rect)

        # Draw the blue footer bar
        footer_bar_rect = pygame.Rect(0, screen.get_height() - 60, screen.get_width(), 60)
        pygame.draw.rect(screen, config.BLUE, footer_bar_rect)

        # Render footer text
        footer_surface = config.font_small.render(self.footer_text, True, config.BLACK)
        footer_rect = footer_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
        screen.blit(footer_surface, footer_rect)