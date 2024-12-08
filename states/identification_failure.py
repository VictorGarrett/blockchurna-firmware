from states.state import State
import states.config as config
import sys
import pygame
from threading import Timer
from datetime import datetime
from text_to_speech.text_to_speech import text_to_speech

class IdentificationFailureState(State):
    def __init__(self):
        super().__init__()
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))
        self.counter = 0
        self.title_text = 'FALHA NA IDENTIFICAÇÃO'
        self.instruction_text = 'Tente novamente'
        self.footer_text = "Município - Zona - Seção"
        self.first_render = True
        self.error_count = 0
        
        
    def reset_state(self):   
        print(self.counter)  
        if self.error_count == 2:
            self.next_state = 'TooManyAttempts' 
            self.error_count = 0
            self.first_render = True
        if self.counter == 1:
            self.next_state = "Identification"
            self.counter = 0
            self.first_render = True
            self.error_count += 1
        else: 
            self.timer = Timer(1.0, self.reset_state)
            self.counter += 1
            self.timer.start()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def render(self, screen):
        if self.first_render:
            self.timer = Timer(1.0, self.reset_state)
            self.timer.start()
            self.first_render = False
            text_to_speech("Falha na identificação, tente novamente")
         # Clear screen
        screen.fill(config.WHITE)

        # Render date and time
        datetime_text = datetime.now().strftime("%Y-%m-%d\n%H:%M:%S")
        config.render_multiline_text(datetime_text, config.font_small, config.BLACK, (20, 20), line_spacing=5)


        # Render main title
        title_surface = config.font_large.render(self.title_text, True, config.BLACK)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
        screen.blit(title_surface, title_rect)

        # Render instructions
        instruction_surface = config.font_medium.render(self.instruction_text, True, config.BLACK)
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        screen.blit(instruction_surface, instruction_rect)

        # Draw the blue footer bar
        footer_bar_rect = pygame.Rect(0, screen.get_height() - 60, screen.get_width(), 60)
        pygame.draw.rect(screen, config.BLUE, footer_bar_rect)

        # Render footer text
        footer_surface = config.font_small.render(self.footer_text, True, config.BLACK)
        footer_rect = footer_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
        screen.blit(footer_surface, footer_rect)

