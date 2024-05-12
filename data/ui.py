import pygame
from data.constants import *
from data.server import start_server, stop_server

class UI:
    def __init__(self, window, timer_manager):
        self.window = window
        self.timer_manager = timer_manager
        self.current_timer_index = 0
        self.font_bold = pygame.font.Font(None, 500)
        self.font_italic = pygame.font.Font(None, 200)
        self.font_button = pygame.font.Font(None, 22)
        self.font_checkbox = pygame.font.Font(None, 16)
        self.font_timer_name = pygame.font.Font(None, 30)
        self.checkbox_rect = pygame.Rect(20, 20, CHECKBOX_WIDTH, CHECKBOX_HEIGHT)
        self.checkbox_label = self.font_checkbox.render("Remote", True, WHITE)
        self.update_button_positions()
        self.server_running = False

    def update_button_positions(self):
        window_width, window_height = self.window.get_size()
        button_y = window_height - BUTTON_HEIGHT - 20
        button_width = (window_width - 6 * BUTTON_SPACING) // 7

        # Start/Stop, Reset, +15 min, +15 sec buttons
        self.start_stop_button_rect = pygame.Rect(BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)
        self.reset_button_rect = pygame.Rect(self.start_stop_button_rect.right + BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)
        self.add_15_min_button_rect = pygame.Rect(self.reset_button_rect.right + BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)
        self.add_15_sec_button_rect = pygame.Rect(self.add_15_min_button_rect.right + BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)

        # Smaller "Previous Timer" and "Next Timer" buttons
        self.prev_timer_button_rect = pygame.Rect(window_width - 2 * button_width - BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)
        self.next_timer_button_rect = pygame.Rect(window_width - button_width, button_y, button_width, BUTTON_HEIGHT)

    def handle_mouse_event(self, pos):
        current_timer = self.timer_manager.timers[self.current_timer_index]
        if self.start_stop_button_rect.collidepoint(pos):
            if current_timer.running:
                current_timer.pause()
            else:
                current_timer.start()
        elif self.reset_button_rect.collidepoint(pos):
            current_timer.reset()
        elif self.add_15_min_button_rect.collidepoint(pos):
            current_timer.add_time(900)
        elif self.add_15_sec_button_rect.collidepoint(pos):
            current_timer.add_time(15)
        elif self.prev_timer_button_rect.collidepoint(pos):
            self.current_timer_index = (self.current_timer_index - 1) % len(self.timer_manager.timers)
        elif self.next_timer_button_rect.collidepoint(pos):
            self.current_timer_index = (self.current_timer_index + 1) % len(self.timer_manager.timers)
        elif self.current_timer_index == 0 and self.checkbox_rect.collidepoint(pos):
            if self.server_running:
                stop_server()
                self.server_running = False
            else:
                start_server(current_timer)
                self.server_running = True

    def update(self):
        self.window.fill(BLACK)
        self.draw_countdown_text()
        self.draw_buttons()
        self.draw_checkbox()
        self.draw_timer_name()

    def draw_countdown_text(self):
        current_timer = self.timer_manager.timers[self.current_timer_index]
        text_colour = self.get_text_colour(current_timer)
        text_minutes = self.font_bold.render(f"{current_timer.minutes:02d}", True, text_colour)
        text_seconds = self.font_italic.render(f"{current_timer.seconds:02d}", True, text_colour)
        text_surface = pygame.Surface((text_minutes.get_width() + text_seconds.get_width() + 20, text_minutes.get_height()), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))
        text_surface.blit(text_minutes, (0, 0))
        text_surface.blit(text_seconds, (text_minutes.get_width() + 20, 20))
        window_width, window_height = self.window.get_size()
        text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2 - 50))
        self.window.blit(text_surface, text_rect)

    def get_text_colour(self, timer):
        if timer.expired and timer.counting_up:
            return RED
        elif not timer.expired and not timer.counting_up:
            if timer.minutes * 60 + timer.seconds <= 300:
                return YELLOW
            else:
                return GREEN
        else:
            return RED

    def draw_buttons(self):
        start_stop_text = self.font_button.render("Start/Stop", True, WHITE)
        reset_text = self.font_button.render("Reset", True, WHITE)
        add_15_min_text = self.font_button.render("+15 min", True, WHITE)
        add_15_sec_text = self.font_button.render("+15 sec", True, WHITE)
        prev_timer_text = self.font_button.render("<", True, WHITE)
        next_timer_text = self.font_button.render(">", True, WHITE)
        pygame.draw.rect(self.window, GREEN2 if self.timer_manager.timers[self.current_timer_index].running else RED, self.start_stop_button_rect)
        pygame.draw.rect(self.window, GREY, self.reset_button_rect)
        pygame.draw.rect(self.window, GREY, self.add_15_min_button_rect)
        pygame.draw.rect(self.window, GREY, self.add_15_sec_button_rect)
        pygame.draw.rect(self.window, GREY, self.prev_timer_button_rect)
        pygame.draw.rect(self.window, GREY, self.next_timer_button_rect)
        self.window.blit(start_stop_text, (self.start_stop_button_rect.x + self.start_stop_button_rect.width // 2 - start_stop_text.get_width() // 2, self.start_stop_button_rect.y + self.start_stop_button_rect.height // 2 - start_stop_text.get_height() // 2))
        self.window.blit(reset_text, (self.reset_button_rect.x + self.reset_button_rect.width // 2 - reset_text.get_width() // 2, self.reset_button_rect.y + self.reset_button_rect.height // 2 - reset_text.get_height() // 2))
        self.window.blit(add_15_min_text, (self.add_15_min_button_rect.x + self.add_15_min_button_rect.width // 2 - add_15_min_text.get_width() // 2, self.add_15_min_button_rect.y + self.add_15_min_button_rect.height // 2 - add_15_min_text.get_height() // 2))
        self.window.blit(add_15_sec_text, (self.add_15_sec_button_rect.x + self.add_15_sec_button_rect.width // 2 - add_15_sec_text.get_width() // 2, self.add_15_sec_button_rect.y + self.add_15_sec_button_rect.height // 2 - add_15_sec_text.get_height() // 2))
        self.window.blit(prev_timer_text, (self.prev_timer_button_rect.x + self.prev_timer_button_rect.width // 2 - prev_timer_text.get_width() // 2, self.prev_timer_button_rect.y + self.prev_timer_button_rect.height // 2 - prev_timer_text.get_height() // 2))
        self.window.blit(next_timer_text, (self.next_timer_button_rect.x + self.next_timer_button_rect.width // 2 - next_timer_text.get_width() // 2, self.next_timer_button_rect.y + self.next_timer_button_rect.height // 2 - next_timer_text.get_height() // 2))

    def draw_checkbox(self):
        if self.current_timer_index == 0:
            pygame.draw.rect(self.window, WHITE, self.checkbox_rect, 2)
            if self.server_running:
                pygame.draw.rect(self.window, GREEN, (self.checkbox_rect.x + 2, self.checkbox_rect.y + 2, CHECKBOX_WIDTH - 4, CHECKBOX_HEIGHT - 4))

            # Increase the font size for the "Remote" label
            remote_label_font = pygame.font.Font(None, 22)
            remote_label_text = remote_label_font.render("Remote", True, WHITE)
            remote_label_rect = remote_label_text.get_rect(
                topleft=(self.checkbox_rect.right + 10, self.checkbox_rect.top)
            )
            self.window.blit(remote_label_text, remote_label_rect)
        elif self.server_running:
            # Display a visual indication that the server is still running
            pygame.draw.rect(self.window, GREEN, (20, 20, 20, 20))

    def draw_timer_name(self):
        current_timer = self.timer_manager.timers[self.current_timer_index]
        timer_name_text = self.font_timer_name.render(current_timer.name, True, WHITE)
        window_width, window_height = self.window.get_size()
        timer_name_rect = timer_name_text.get_rect(midtop=(window_width // 2, 20))
        self.window.blit(timer_name_text, timer_name_rect)