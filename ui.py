import pygame
from constants import *
from server import start_server, stop_server

class UI:
    def __init__(self, window, timer):
        self.window = window
        self.timer = timer
        self.font_bold = pygame.font.Font(None, 500)
        self.font_italic = pygame.font.Font(None, 200)
        self.font_button = pygame.font.Font(None, 22)
        self.font_checkbox = pygame.font.Font(None, 16)
        self.checkbox_rect = pygame.Rect(20, 20, CHECKBOX_WIDTH, CHECKBOX_HEIGHT)
        self.checkbox_label = self.font_checkbox.render("Remote", True, WHITE)
        self.update_button_positions()
        self.server_running = False

    def update_button_positions(self):
        window_width, window_height = self.window.get_size()
        button_y = window_height - BUTTON_HEIGHT - 20
        button_width = (window_width - 3 * BUTTON_SPACING) // 4
        self.start_stop_button_rect = pygame.Rect((window_width - 4 * button_width - 3 * BUTTON_SPACING) // 2, button_y, button_width, BUTTON_HEIGHT)
        self.reset_button_rect = pygame.Rect(self.start_stop_button_rect.right + BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)
        self.add_15_min_button_rect = pygame.Rect(self.reset_button_rect.right + BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)
        self.add_15_sec_button_rect = pygame.Rect(self.add_15_min_button_rect.right + BUTTON_SPACING, button_y, button_width, BUTTON_HEIGHT)

    def handle_mouse_event(self, pos):
        if self.start_stop_button_rect.collidepoint(pos):
            if self.timer.running:
                self.timer.pause()
            else:
                self.timer.start()
        elif self.reset_button_rect.collidepoint(pos):
            self.timer.reset()
        elif self.add_15_min_button_rect.collidepoint(pos):
            self.timer.add_time(900)
        elif self.add_15_sec_button_rect.collidepoint(pos):
            self.timer.add_time(15)
        elif self.checkbox_rect.collidepoint(pos):
            if self.server_running:
                stop_server()
                self.server_running = False
            else:
                start_server(self.timer)
                self.server_running = True

    def update(self):
        self.window.fill(BLACK)
        self.draw_countdown_text()
        self.draw_buttons()
        self.draw_checkbox()

    def draw_countdown_text(self):
        text_colour = self.get_text_colour()
        text_minutes = self.font_bold.render(f"{self.timer.minutes:02d}", True, text_colour)
        text_seconds = self.font_italic.render(f"{self.timer.seconds:02d}", True, text_colour)
        text_surface = pygame.Surface((text_minutes.get_width() + text_seconds.get_width() + 20, text_minutes.get_height()), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))
        text_surface.blit(text_minutes, (0, 0))
        text_surface.blit(text_seconds, (text_minutes.get_width() + 20, 20))
        window_width, window_height = self.window.get_size()
        text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2))
        self.window.blit(text_surface, text_rect)

    def get_text_colour(self):
        if self.timer.expired and self.timer.counting_up:
            return RED
        elif not self.timer.expired and not self.timer.counting_up:
            if self.timer.minutes * 60 + self.timer.seconds <= 300:
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
        pygame.draw.rect(self.window, GREEN2 if self.timer.running else RED, self.start_stop_button_rect)
        pygame.draw.rect(self.window, GREY, self.reset_button_rect)
        pygame.draw.rect(self.window, GREY, self.add_15_min_button_rect)
        pygame.draw.rect(self.window, GREY, self.add_15_sec_button_rect)
        self.window.blit(start_stop_text, (self.start_stop_button_rect.x + self.start_stop_button_rect.width // 2 - start_stop_text.get_width() // 2, self.start_stop_button_rect.y + self.start_stop_button_rect.height // 2 - start_stop_text.get_height() // 2))
        self.window.blit(reset_text, (self.reset_button_rect.x + self.reset_button_rect.width // 2 - reset_text.get_width() // 2, self.reset_button_rect.y + self.reset_button_rect.height // 2 - reset_text.get_height() // 2))
        self.window.blit(add_15_min_text, (self.add_15_min_button_rect.x + self.add_15_min_button_rect.width // 2 - add_15_min_text.get_width() // 2, self.add_15_min_button_rect.y + self.add_15_min_button_rect.height // 2 - add_15_min_text.get_height() // 2))
        self.window.blit(add_15_sec_text, (self.add_15_sec_button_rect.x + self.add_15_sec_button_rect.width // 2 - add_15_sec_text.get_width() // 2, self.add_15_sec_button_rect.y + self.add_15_sec_button_rect.height // 2 - add_15_sec_text.get_height() // 2))

    def draw_checkbox(self):
        pygame.draw.rect(self.window, WHITE, self.checkbox_rect, 2)
        if self.server_running:
            pygame.draw.rect(self.window, GREEN, (self.checkbox_rect.x + 2, self.checkbox_rect.y + 2, CHECKBOX_WIDTH - 4, CHECKBOX_HEIGHT - 4))
        self.window.blit(self.checkbox_label, (self.checkbox_rect.x + CHECKBOX_WIDTH + 10, self.checkbox_rect.y))