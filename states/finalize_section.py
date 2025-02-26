from states.state import State
import states.config as config
import sys
import pygame
from threading import Timer
import time

class FinalizeSection(State):
    def __init__(self):
        super().__init__()
        self.text = config.font.render("Game State - Press ESC to Exit", True, config.text_color)
        self.text_rect = self.text.get_rect(center=(config.screen.get_width() // 2, config.screen.get_height() // 2))
        self.counter = 0 
        self.max_counter = 3
        self.timer_active = False 
        self.session_finalized = False
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

    def reset_state(self):
        if self.counter < self.max_counter:
            self.counter += 1
            self.timer = Timer(1.0, self.reset_state)
            self.timer.start()
        else:
            self.timer_active = False
            self.session_finalized = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def render(self, screen):
        if not self.timer_active and not self.session_finalized:
            self.timer_active = True
            self.timer = Timer(1.0, self.reset_state)
            self.timer.start()

        screen.fill(config.WHITE)

        if self.session_finalized:
            text_final = config.font_large.render("SEÇÃO FINALIZADA.", True, config.BLACK)
            screen.blit(text_final, (config.screen.get_width() // 2 - text_final.get_width() // 2, config.screen.get_height() // 2))
            for event in events:
                if event.type == pygame.KEYDOWN and event.key in self.keyboard_mapping.keys():
                    self.password += self.keyboard_mapping[event.key]
                    print(self.password)
                    if not self.password.startswith("7"):
                        self.password = ""
                    if len(self.password) > 5:
                        self.password = ""
                    if self.password == "77777":
                        pygame.quit()
                        sys.exit()
        else:
            # Text
            text1 = config.font_large.render("FINALIZANDO SEÇÃO...", True, config.BLACK)

            # Progress bar settings
            progress_bar_width = config.screen.get_width() // 1.5
            progress_bar_height = 50
            progress_bar_x = (config.screen.get_width() - progress_bar_width) // 2
            progress_bar_y = config.screen.get_height() // 2 + 30
            progress = self.counter / 3  # 50% filled

            screen.blit(text1, (config.screen.get_width() // 2 - text1.get_width() // 2, 100))
            # Draw progress bar background
            pygame.draw.rect(screen, config.BLACK, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)

            # Draw progress
            pygame.draw.rect(screen, config.GREEN, (progress_bar_x, progress_bar_y, progress * progress_bar_width, progress_bar_height))

        