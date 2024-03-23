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

# Create the timer and UI objects
timer = Timer(INITIAL_COUNTDOWN)
ui = UI(window, timer)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            ui.handle_mouse_event(pos)
        elif event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            ui.window = window
            ui.update_button_positions()

    timer.update()
    ui.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()