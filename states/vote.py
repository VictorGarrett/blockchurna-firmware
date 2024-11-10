from states.state import State
import states.config as config
import pygame
import sys

def get_candidate_image(filepath: str): 
    candidate_1_image = pygame.image.load(f"./assets/{filepath}")
    return pygame.transform.scale(candidate_1_image, (220, 250))
     

candidates = {
    "Vereador": {
        "91001": {
            "image": get_candidate_image("diogenes.png"),
            "name": "Diogenes Nascimento",
            "party": "Partido Super Tchurus Cobol"
        },
        "36500": {
            "image": get_candidate_image("socrates.png"),
            "name": "Socrates Paqueta",
            "party": "Partido da BET"
        }
    },
    "Prefeito": {
        "91": {
            "image": get_candidate_image("saci.png"),
            "name": "Saci Junior",
            "party": "Partido Super Tchurus Cobol"
        },
        "36": {
            "image": get_candidate_image("medusa.png"),
            "name": "Medusa Cafusa",
            "party": "Partido da BET"
        }
    }
    
}


class VoteState(State):
    def __init__(self, position: str, candidate_number_size: int, next_state: str):
        super().__init__()
        self.title_text = "Seu voto para"
        self.position_text = position
        self.candidate_number = " " * candidate_number_size
        self.candidate_number_size = candidate_number_size
        self.current_digit = 0
        self.candidate_photo_text = "FOTO\nDO\nCANDIDATO"
        self.white_vote = False
        self.can_confirm = False
        self.next_state_to_go = next_state


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    self.candidate_number = " " * self.candidate_number_size
                    self.white_vote = False
                    self.current_digit = 0
                elif event.key in range(pygame.K_0, pygame.K_9 + 1):  # Number keys 0-9
                    candidate_number = list(self.candidate_number)
                    if self.current_digit < self.candidate_number_size:
                        candidate_number[self.current_digit] = str(event.key - pygame.K_0)  # Convert key to char
                        self.current_digit += 1
                    self.candidate_number = ''.join(candidate_number)
                elif event.key == pygame.K_SPACE:
                    self.white_vote = True
                elif event.key == pygame.K_RETURN and self.can_confirm:
                    self.next_state = self.next_state_to_go
                    self.candidate_number = " " * self.candidate_number_size
                    config.pirilim_candidate.play()
                    self.current_digit = 0

    def render(self, screen):
        self.candidate = None
        # print(f"({self.candidate_number})")
        if self.candidate_number in candidates[self.position_text]:
            self.candidate = candidates[self.position_text][self.candidate_number]
        
        screen.fill(config.WHITE)

        # Render title text
        title_surface = config.font_small.render(self.title_text, True, config.BLACK)
        screen.blit(title_surface, (20, 20))

        # Render "Cargo" label
        position_surface = config.font_medium.render(self.position_text, True, config.BLACK)
        screen.blit(position_surface, (50, 70))

        # Draw the input boxes for the candidate number
        box_x = 50
        box_y = 120
        box_width = 60
        box_height = 100
        box_spacing = 10

        rect_left, rect_top, rect_width, rect_height = 530, 50, 220, 250 
        photo_rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)

        if not self.white_vote:
            for i, digit in enumerate(self.candidate_number):
                pygame.draw.rect(screen, config.BLACK, (box_x + i * (box_width + box_spacing), box_y, box_width, box_height), 2)
                digit_surface = config.font_extra_large.render(digit, True, config.BLACK)
                screen.blit(digit_surface, (box_x + i * (box_width + box_spacing) + 10, box_y + 16))


            pygame.draw.rect(screen, config.BLACK, photo_rect, 2)

        if " " in self.candidate_number and not self.white_vote:
            self.can_confirm = False
            config.render_multiline_text(self.candidate_photo_text, config.font_medium, config.BLACK, (photo_rect.x + 40, photo_rect.y + 80), 5)
    
        else:
            self.can_confirm = True
            if self.white_vote:
                white_vote_surface = config.font_very_large.render("VOTO EM BRANCO", True, config.BLACK)
                text_rect = white_vote_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
                screen.blit(white_vote_surface, text_rect)
            elif self.candidate:
                party_surface = config.font_medium.render("Nome: " + self.candidate["name"], True, config.BLACK)
                screen.blit(party_surface, (50, 260))

                party_surface = config.font_medium.render("Partido: " + self.candidate["party"], True, config.BLACK)
                screen.blit(party_surface, (50, 300))

                config.screen.blit(self.candidate["image"], (530, 50))
            else:
                null_surface = config.font_very_large.render("X", True, config.BLACK)
                screen.blit(null_surface, (rect_left + rect_width // 2 - 22, rect_top + rect_height // 2- 22))
                wrong_number_surface = config.font_medium.render("NÚMERO ERRADO", True, config.BLACK)
                null_vote_surface = config.font_very_large.render("VOTO NULO", True, config.BLACK)
                text_rect = null_vote_surface.get_rect(center=(screen.get_width() // 2, 360))
                screen.blit(wrong_number_surface, (50, 250))
                screen.blit(null_vote_surface, text_rect)

            # Renderiza as instruções de confirmação
            confirm_instruction = "CONFIRMA para CONFIRMAR este voto"
            correct_instruction = "CORRIGE para REINICIAR este voto"
            footer_text = "Aperte a tecla:"
            footer_surface = config.font_small.render(footer_text, True, config.BLACK)
            confirm_surface = config.font_small.render(confirm_instruction, True, config.BLACK)
            correct_surface = config.font_small.render(correct_instruction, True, config.BLACK)
            screen.blit(footer_surface, (30, 400))
            screen.blit(confirm_surface, (50, 425))
            screen.blit(correct_surface, (50, 450))

            pygame.draw.line(screen, config.BLACK, (0, 390), (config.screen.get_width(), 390), 2)

        # Update display
        pygame.display.flip()
