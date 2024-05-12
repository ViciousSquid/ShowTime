import pygame
from data.timer import Timer
from data.timer_manager import TimerManager
from data.ui import UI
from data.server import start_server, stop_server
from data.constants import WINDOW_WIDTH, WINDOW_HEIGHT, TIMERS

# Initialize Pygame
pygame.init()

# Set up the initial window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ShowTime")

# Create the TimerManager and UI objects
timer_manager = TimerManager(TIMERS)
ui = UI(window, timer_manager)

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

    timer_manager.update_timers()
    ui.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()