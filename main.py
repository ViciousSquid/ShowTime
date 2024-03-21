import pygame
from timer import Timer
from ui import UI
from server import start_server, stop_server
from constants import *

# Initialize Pygame
pygame.init()

# Set up the initial window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ShowTime")

# Set up the timer
timer = Timer(INITIAL_COUNTDOWN)

# Set up the UI
ui = UI(window, timer)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ui.handle_mouse_event(event.pos)

    timer.update()
    ui.update()

    pygame.display.update()

# Quit Pygame
pygame.quit()