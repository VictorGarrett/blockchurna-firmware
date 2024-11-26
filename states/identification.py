from states.state import State
import states.config as config
from datetime import datetime
import sys
import pygame
import random
from flash_memory.flash_memory import FlashMemory
keys = [
    "2ab9701cc00c33993ac0",
    "6bdd705a76a16b34bdbf",
    "07b8e21175c2e1b733b4",
    "7fda43f45060db9f3d7d",
    "8cba4d7c64f0c1c52519",
    "57ca2eda39d9f560133b",
    "61c69ed4d53b08b4ba44",
    "78f8959451146bfbb771",
    "88f73783487b326c035f",
    "514eb8dbe1339bbc2ec5",
    "648477f3600689714007",
    "919363b1d8846f0037ed",
    "a622942949441e508eaf",
    "b24bdb1813dc5cb6e119",
    "b4024aa146301c0073b6",
    "debc4efe43dbd3847f20",
    "fb4623e58bf05a2325ee",
    "fd8ab23f1d9ba1e7e100"
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