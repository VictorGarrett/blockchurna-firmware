from states.state import State
import states.config as config
import pygame
import sys
from flash_memory.flash_memory import FM
# from gpio.gpio import GPIO 
from text_to_speech.text_to_speech import text_to_speech
from biometry.add_fingerprint import enroll_fingerprint_with_sensor

# gpio = GPIO()

class EnrollFinger(State):
    def __init__(self, finger_sensor):
        super().__init__()
        self.finger_sensor = finger_sensor
        self.title_text = "id da digital"
        self.candidate_number = " " * 2
        self.candidate_number_size = 2
        self.current_digit = 0
        self.candidate_photo_text = "QUADRADO"
        self.white_vote = False
        self.can_confirm = False
        self.first_render = True
        self.should_play_audio = False 
        self.audio_text = ""
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.key in self.keyboard_mapping.keys():  # Number keys 0-9
                    candidate_number = list(self.candidate_number)
                    if self.current_digit < self.candidate_number_size:
                        candidate_number[self.current_digit] = self.keyboard_mapping[event.key]  # Convert key to char
                        self.current_digit += 1
                    self.candidate_number = ''.join(candidate_number)
                    self.should_play_audio = True

    def update(self):
        if gpio.gpio_check(gpio.GPIO_CORREGE):
            self.candidate_number = " " * self.candidate_number_size
            self.white_vote = False
            self.current_digit = 0

        elif gpio.gpio_check(gpio.GPIO_CONFIRMA) and self.can_confirm:
            if enroll_fingerprint_with_sensor(self.candidate_number, self.finger_sensor) < 0:
                self.next_state = 'IdentificationFailure'
            else:
                self.next_state = 'Identification'
        elif gpio.gpio_check(gpio.GPIO_BRANCO):
            self.white_vote = True

    def render(self, screen):
        if self.first_render:
            self.first_render=False
            #text_to_speech(f"Você está votando para {self.position_text}")

        if self.should_play_audio == True and self.audio_text:
            print("text")
            self.should_play_audio = False 
            #text_to_speech(self.audio_text)
            self.audio_text = ""

        self.candidate = None
        # print(f"({self.candidate_number})")
        
        screen.fill(config.WHITE)

        # Render title text
        title_surface = config.font_small.render(self.title_text, True, config.BLACK)
        screen.blit(title_surface, (20, 20))


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
                self.audio_text = "Voto branco, clique em confirmar"
                white_vote_surface = config.font_very_large.render("VOTO EM BRANCO", True, config.BLACK)
                text_rect = white_vote_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
                screen.blit(white_vote_surface, text_rect)
            elif self.candidate:
                self.audio_text = f"{self.candidate_number}, candidato {self.candidate['name']}, do {self.candidate['party']}, clique em confirma para votar, ou corrége para alterar."

                party_surface = config.font_medium.render("Nome: " + self.candidate["name"], True, config.BLACK)
                screen.blit(party_surface, (50, 260))

                party_surface = config.font_medium.render("Partido: " + self.candidate["party"], True, config.BLACK)
                screen.blit(party_surface, (50, 300))

                config.screen.blit(self.candidate["image"], (530, 50))
            else:
                self.audio_text = "Candidato não encontrado, clique em confirmar para votar nulo, ou aperte corrige para alterar."

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

