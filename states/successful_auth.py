from gpio.gpio import gpio
from states.state import State
import states.config as config
import sys
import pygame
from threading import Timer
from datetime import datetime
from text_to_speech.text_to_speech import text_to_speech
from flash_memory.flash_memory import FM

class SuccessfulAuthState(State):
    def __init__(self):
        super().__init__()
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))
        self.counter = 0
        self.title_text = 'AUTENTICADO COM SUCESSO'
        self.intruction_text_1 = 'Aperte CONFIRMA para confirmar sua identidade'
        self.intruction_text_2 = 'ou aperte CORREGE para identificar-se novamente'


        self.footer_text = "Município - Zona - Seção"
        self.first_render = True
        
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # registrar presença na flash memory
                # self.first_render = True
                self.next_state = 'Vote Vereador'
                FM.register_presence()
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                # registrar presença na flash memory
                # self.first_render = True
                self.next_state = 'Identification'

    def update(self):
        if gpio.gpio_check(gpio.GPIO_CORREGE):
            # self.first_render = True
            self.next_state = 'Identification'
        elif gpio.gpio_check(gpio.GPIO_CONFIRMA):
            # self.first_render = True
            self.next_state = 'Vote Vereador'
            FM.register_presence()

    def render(self, screen):
        voter_name = FM.current_voter["name"]
        self.subtitle_text = voter_name
        # text_to_speech(f"Autenticado com sucesso, {voter_name}, aperte confirma para confirmar sua identidade ou aperte correge para identificar-se novamente")
        # self.first_render = False
         # Clear screen
        screen.fill(config.WHITE)

        # Render date and time
        datetime_text = datetime.now().strftime("%Y-%m-%d\n%H:%M:%S")
        config.render_multiline_text(datetime_text, config.font_small, config.BLACK, (20, 20), line_spacing=5)


        # Render main title
        title_surface = config.font_large.render(self.title_text, True, config.BLACK)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60))
        screen.blit(title_surface, title_rect)

        subtitle_surface = config.font_large.render(self.subtitle_text, True, config.BLACK)
        subtitle_rect = subtitle_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(subtitle_surface, subtitle_rect)

        # Render instructions
        instruction_surface = config.font_medium.render(self.intruction_text_1, True, config.BLACK)
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(instruction_surface, instruction_rect)

        instruction2_surface = config.font_medium.render(self.intruction_text_2, True, config.BLACK)
        instruction2_rect = instruction_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 90))
        screen.blit(instruction2_surface, instruction2_rect)

        # Draw the blue footer bar
        footer_bar_rect = pygame.Rect(0, screen.get_height() - 60, screen.get_width(), 60)
        pygame.draw.rect(screen, config.BLUE, footer_bar_rect)

        # Render footer text
        footer_surface = config.font_small.render(self.footer_text, True, config.BLACK)
        footer_rect = footer_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
        screen.blit(footer_surface, footer_rect)

