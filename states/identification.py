from states.state import State
import states.config as config
from datetime import datetime
import sys
import pygame
import random
from flash_memory.flash_memory import FlashMemory
from biometry.fingerprint_sensor import FingerprintSensor
keys = [
    "0bea05cf004534d9cc8c",
    "01b8b186a1d869910136",
    "5b5a6ffb5ddb48097f1f",
    "7b3470be2b9cf73957e8",
    "9f2e4b1356c648e1a2aa",
    "10b82744669347897ab5",
    "14f4e0a1a724842873e2",
    "50a4be92c301dc113063",
    "56f326b0e23fb765963f",
    "71df18ad8337037d720a",
    "090adfab610ac04c63ab",
    "708e6f27e52e476cfe1d",
    "781ae0d88daa1bbd7b4a",
    "5887c27b14664077e318",
    "8788f46a439f4f718757",
    "a5ec5c49eef382efcc1e",
    "b46338b9eb513bfaafc5",
    "c6f07accdb016a24396e"
]
class IdentificationState(State):
    def __init__(self):
        super().__init__()
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))

        self.title_text = "INÍCIO DA VOTAÇÃO"
        self.instruction_text = "Por favor se identifique através da digital"
        self.footer_text = "Município - Zona - Seção"
        self.password = ""


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # registrar presença na flash memory
                random_key = random.choice(keys)
                FlashMemory.register_presence(random_key)
                self.next_state = "Vote Vereador" 
            elif event.type == pygame.KEYDOWN and (event.key in range(pygame.K_0, pygame.K_9 + 1)):
                self.password += str(event.key - pygame.K_0) 
                with open("flash_memory/password.txt", "r") as pw:
                    ballot_pw = pw.read()
                if self.password == ballot_pw:
                    self.next_state = "Finalize Section"
                    FlashMemory.sign_ballot()
                    pass

    def update(self):
        key = FingerprintSensor.get_user_from_fingerprint()
        if key:
            FlashMemory.register_presence(key)

                
    def render(self, screen):
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