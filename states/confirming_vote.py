from printer.print_vote_receipt import print_vote_receipt
from states.state import State
import states.config as config
import sys
import pygame
from threading import Timer
from flash_memory.flash_memory import FM
from gpio.gpio import gpio 

from text_to_speech.text_to_speech import text_to_speech

class ConfirmingVote(State):
    def __init__(self):
        super().__init__()
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))
        self.counter = 0

        self.first_render = True
        
        
    def reset_state(self):     
        if self.counter == 3:
            self.next_state = "End"
            self.first_render = True
        else: 
            self.timer = Timer(1.0, self.reset_state)
            self.counter += 1
            self.timer.start()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def update(self):
        if gpio.gpio_check(gpio.GPIO_CORREGE):
            print_vote_receipt(FM.current_voter["key_id"], FM.current_voter["name"], FM.user_data[-2]["pin"], FM.user_data[-1]["pin"])

        elif gpio.gpio_check(gpio.GPIO_CONFIRMA) and self.can_confirm:
            self.next_state = "End"
            self.first_render = True
            
        elif gpio.gpio_check(gpio.GPIO_BRANCO):
            pass

    def render(self, screen):
        if self.first_render:
            self.timer = Timer(1.0, self.reset_state)
            self.timer.start()
            # text_to_speech(f"Gravando voto e gerando comprovante")
            print_vote_receipt(FM.current_voter["key_id"], FM.current_voter["name"], FM.user_data[-2]["pin"], FM.user_data[-1]["pin"])
            self.first_render = False

        screen.fill(config.WHITE)
        # Text
        text1 = config.font_large.render("GRAVANDO O VOTO", True, config.BLACK)
        text2 = config.font_large.render("e", True, config.BLACK)
        text3 = config.font_large.render("GERANDO COMPROVANTE", True, config.BLACK)

        # Progress bar settings
        progress_bar_width = config.screen.get_width() // 1.5
        progress_bar_height = 50
        progress_bar_x = (config.screen.get_width() - progress_bar_width) // 2
        progress_bar_y = config.screen.get_height() // 2 + 30
        progress = self.counter / 3  # 50% filled

        screen.blit(text1, (config.screen.get_width() // 2 - text1.get_width() // 2, 100))
        screen.blit(text2, (config.screen.get_width() // 2 - text2.get_width() // 2, 140))
        screen.blit(text3, (config.screen.get_width() // 2 - text3.get_width() // 2, 180))
        
        # Draw progress bar background
        pygame.draw.rect(screen, config.BLACK, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)

        # Draw progress
        pygame.draw.rect(screen, config.GREEN, (progress_bar_x, progress_bar_y, progress * progress_bar_width, progress_bar_height))

        # Renderiza as instruções de confirmação
        footer_text = "Aperte a tecla:"
        confirm_instruction = "CONFIRMA para FINALIZAR"
        correct_instruction = "CORRIGE para IMPRIMIR comprovante novamente"

        footer_surface = config.font_small.render(footer_text, True, config.BLACK)
        confirm_surface = config.font_small.render(confirm_instruction, True, config.BLACK)
        correct_surface = config.font_small.render(correct_instruction, True, config.BLACK)

        screen.blit(footer_surface, (30, 400))
        screen.blit(confirm_surface, (50, 425))
        screen.blit(correct_surface, (50, 450))

        pygame.draw.line(screen, config.BLACK, (0, 390), (config.screen.get_width(), 390), 2)


