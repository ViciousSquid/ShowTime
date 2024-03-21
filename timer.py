import pygame
from constants import *

class Timer:
    def __init__(self, initial_countdown):
        self.initial_countdown = initial_countdown
        self.reset()

    def reset(self):
        self.countdown = self.initial_countdown
        self.start_ticks = pygame.time.get_ticks()
        self.expired = False
        self.counting_up = False
        self.running = False
        self.paused_time = 0

    def start(self):
        self.running = True
        if self.paused_time:
            self.start_ticks += pygame.time.get_ticks() - self.paused_time
            self.paused_time = 0

    def pause(self):
        self.running = False
        self.paused_time = pygame.time.get_ticks()

    def add_time(self, seconds):
        if self.running:
            self.countdown += seconds
        else:
            self.countdown += seconds

    def update(self):
        if self.running:
            elapsed_time = pygame.time.get_ticks() - self.start_ticks - self.paused_time
            if not self.counting_up:
                remaining_time = max(self.countdown - elapsed_time // 1000, 0)
            else:
                remaining_time = elapsed_time // 1000
        else:
            remaining_time = max(self.countdown - (self.paused_time - self.start_ticks) // 1000, 0)

        if remaining_time <= 0:
            if not self.counting_up:
                self.expired = True
                self.counting_up = True
                self.start_ticks = pygame.time.get_ticks()

        self.minutes = remaining_time // 60
        self.seconds = remaining_time % 60