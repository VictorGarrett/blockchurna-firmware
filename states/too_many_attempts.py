from states.state import State
import states.config as config
import sys
import pygame
from threading import Timer
from datetime import datetime
from text_to_speech.text_to_speech import text_to_speech

class TooManyAttemptsState(State):
    def __init__(self):
        super().__init__()
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))
        self.counter = 0
        self.title_text = 'MUITAS FALHAS CONSECUTIVAS'
        self.instruction_text = 'Comunique o mesário da seção'
        self.footer_text = "Município - Zona - Seção"
        self.first_render = True
        self.password = ""
        self.keyboard_mapping = {
            1073741913: "7",
            1073741914: "8",
            1073741915: "9",
            1073741916: "4",
            1073741917: "5",
            1073741918: "6",
            1073741919: "1",
            1073741920: "2",
            1073741921: "3",
            1073741922: "0",
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in self.keyboard_mapping.keys():
                self.password += self.keyboard_mapping[event.key]
                print(self.password)
                if not self.password.startswith("7"):
                    self.password = ""
                if len(self.password) > 5:
                    self.password = ""
                if self.password == "77777":
                    self.next_state = "Identification"
                    self.first_render = True


    def render(self, screen):
        if self.first_render:
            self.counter = 5
            # text_to_speech("Muitas falhas consecutivas, comunique o mesário da seção")
            self.first_render = False
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

