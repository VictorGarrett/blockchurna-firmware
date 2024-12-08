from states.state import State
import states.config as config
from datetime import datetime
import sys
import pygame
import random
import json
from flash_memory.flash_memory import FM
from text_to_speech.text_to_speech import text_to_speech

def load_voter_keys_mapping(json_file):

    with open(json_file, 'r', encoding='utf-8') as file:
        keys = json.load(file)
    
    return keys

class IdentificationState(State):
    def __init__(self, finger_sensor):
        super().__init__()
        self.finger = finger_sensor
        self.voter_info = load_voter_keys_mapping("./keys.json")
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))

        self.title_text = "INÍCIO DA VOTAÇÃO"
        self.instruction_text = "Por favor se identifique através da digital"
        self.footer_text = "Município - Zona - Seção"
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # registrar presença na flash memory
                # current_voter = random.choice(keys)
                current_voter = self.voter_info[0]
                if current_voter["key_id"] in FM.already_voted:
                    self.next_state = "AlreadyVoted"
                else:
                    FM.set_current_voter(current_voter)
                    self.next_state = "SuccessfulAuth"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.next_state = "IdentificationFailure" 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                self.next_state = "AlreadyVoted" 
            elif event.type == pygame.KEYDOWN and event.key in self.keyboard_mapping.keys():
                self.password += self.keyboard_mapping[event.key]
                
                if not self.password.startswith("7"):

                    self.password = "" 
                with open("flash_memory/password.txt", "r") as pw:
                    ballot_pw = pw.read()
                if self.password == ballot_pw:
                    self.next_state = "Finalize Section"
                    FM.sign_ballot()
                    pass
                if self.password == '72345':
                    self.password = "" 
                    self.next_state = "EnrollFinger"
                    pass

    def update(self):
        key = self.finger.get_user_from_fingerprint()
        if key:
            if key >= 0:
                if key in FM.already_voted:
                    self.next_state = "AlreadyVoted"
                else:
                    FM.set_current_voter(self.voter_info[key])
                    self.next_state = "SuccessfulAuth" 
            else:
                 self.next_state = "IdentificationFailure"
                
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