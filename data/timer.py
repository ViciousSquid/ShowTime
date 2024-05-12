import pygame
from .constants import *

class Timer:
    def __init__(self, initial_countdown, name):
        self.initial_countdown = initial_countdown
        self.name = name
        self.reset()

    def reset(self):
        self.countdown = self.initial_countdown
        self.start_ticks = None
        self.expired = False
        self.counting_up = False
        self.running = False
        self.paused_time = 0

    def start(self):
        self.running = True
        if self.start_ticks is None:  # If the timer hasn't started yet
            self.start_ticks = pygame.time.get_ticks()
        elif self.paused_time:
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
            if self.start_ticks is not None:  # Check if the timer has started
                elapsed_time = pygame.time.get_ticks() - self.start_ticks - self.paused_time
                if not self.counting_up:
                    remaining_time = max(self.countdown - elapsed_time // 1000, 0)
                else:
                    remaining_time = elapsed_time // 1000
            else:  # Timer hasn't started yet, so remaining time is the initial countdown
                remaining_time = self.countdown
        else:
            if self.start_ticks is not None:  # Check if the timer has started before
                remaining_time = max(self.countdown - (self.paused_time - self.start_ticks) // 1000, 0)
            else:  # Timer hasn't started yet, so remaining time is the initial countdown
                remaining_time = self.countdown

        if remaining_time <= 0:
            if not self.counting_up:
                self.expired = True
                self.counting_up = True
                self.start_ticks = pygame.time.get_ticks()

        self.minutes = remaining_time // 60
        self.seconds = remaining_time % 60