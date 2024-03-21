#
# THIS WAS ORIGINALLY THE MASTER FILE
# IT WAS SPLIT INTO MULTIPLE FILES FOR VERSION 1.1
# AND THIS MASTER FILE IS NOW DEPRECIATED
#


print("*** Showtime Starting up...")
print(" ")
print("LOG: Loading libraries...")

import pygame
import threading
import http.server
import socketserver

# Initialize Pygame
pygame.init()

# Set up the initial window
window_width = 1024
window_height = 600
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("ShowTime")

# Define colours
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (147, 197, 114)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 191, 0)
GREY = (40, 40, 43)

# Define font
font = pygame.font.Font(None, 100)          # Smol font
font_bold = pygame.font.Font(None, 500)     # Big font
font_italic = pygame.font.Font(None, 200)   # Medium font
font_button = pygame.font.Font(None, 22)    # Button font
font_checkbox = pygame.font.Font(None, 16)  # Checkbox font

# Set up the countdown
initial_countdown = 899  # 900 secs = 15 minutes
countdown = initial_countdown
start_ticks = pygame.time.get_ticks()
expired = False
counting_up = False
running = False  # Start in paused state
paused_time = 0  # Remember paused time

# Button settings
button_width = 160
button_height = 50
button_spacing = 20

# Checkbox settings
checkbox_width = 20
checkbox_height = 20
checkbox_rect = pygame.Rect(20, 20, checkbox_width, checkbox_height)
checkbox_label = font_checkbox.render("Remote", True, WHITE)

# HTTP server settings
server_running = False
counter_value = ""

class CounterHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(f"<html><body><h1>Timer: {counter_value}</h1></body></html>", "utf-8"))

def update_counter_value():
    global counter_value
    while server_running:
        remaining_time = max(countdown - (pygame.time.get_ticks() - start_ticks - paused_time) // 1000, 0)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        counter_value = f"{minutes:02d}:{seconds:02d}"
        pygame.time.wait(1000)  # Update every second

def start_server():
    global server_running
    server_running = True
    print("LOG: HTTP server running on localhost:8000")
    server = socketserver.TCPServer(("", 8000), CounterHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    counter_thread = threading.Thread(target=update_counter_value)
    counter_thread.start()

def stop_server():
    global server_running
    server_running = False

def update_button_positions(window_width, window_height):
    global start_stop_button_rect, reset_button_rect, add_15_min_button_rect, add_15_sec_button_rect
    button_y = window_height - button_height - 20
    start_stop_button_rect = pygame.Rect(20, button_y, button_width, button_height)
    reset_button_rect = pygame.Rect(window_width // 4 - button_width // 2, button_y, button_width, button_height)
    add_15_min_button_rect = pygame.Rect(window_width // 2 - button_width // 2, button_y, button_width, button_height)
    add_15_sec_button_rect = pygame.Rect(3 * window_width // 4 - button_width // 2, button_y, button_width, button_height)

update_button_positions(window_width, window_height)  # Call the function to initialize button rects

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if server_running:
                stop_server()
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_stop_button_rect.collidepoint(mouse_pos):
                running = not running
                if running:  # If resuming, adjust start_ticks to exclude paused time
                    start_ticks += pygame.time.get_ticks() - paused_time
                    paused_time = 0
                else:  # If pausing, record the current time
                    paused_time = pygame.time.get_ticks()
            elif reset_button_rect.collidepoint(mouse_pos):
                countdown = initial_countdown  # Reset countdown to initial value
                start_ticks = pygame.time.get_ticks()  # Reset start_ticks to current time
                expired = False
                counting_up = False
                if running:  # If running, reset paused time
                    paused_time = 0
            elif add_15_min_button_rect.collidepoint(mouse_pos):
                if running:
                    countdown += 900  # 15 minutes in seconds
                else:
                    # Adjust countdown by directly adding time to it
                    countdown += 899
            elif add_15_sec_button_rect.collidepoint(mouse_pos):
                if running:
                    countdown += 15  # 15 seconds
                else:
                    # Adjust countdown by directly adding time to it
                    countdown += 15
            elif checkbox_rect.collidepoint(mouse_pos):
                if server_running:
                    stop_server()
                else:
                    start_server()

    # Calculate remaining time regardless of whether the timer is running or paused
    if running:
        elapsed_time = pygame.time.get_ticks() - start_ticks - paused_time
        if not counting_up:
            remaining_time = max(countdown - elapsed_time // 1000, 0)
        else:
            remaining_time = elapsed_time // 1000
    else:
        remaining_time = max(countdown - (paused_time - start_ticks) // 1000, 0)

    # Render the countdown text
    minutes = remaining_time // 60
    seconds = remaining_time % 60

    if not expired and not counting_up:
        if remaining_time <= 300:           # When only 5 minutes remaining
            text_colour = YELLOW            # Change the text colour to yellow
        else:
            text_colour = GREEN
    else:
        text_colour = RED

    # Render minutes and seconds separately with different styles
    text_minutes = font_bold.render(f"{minutes:02d}", True, text_colour)
    text_seconds = font_italic.render(f"{seconds:02d}", True, text_colour)

    # Create a surface to hold minutes and seconds text
    text_surface = pygame.Surface((text_minutes.get_width() + text_seconds.get_width() + 20, text_minutes.get_height()), pygame.SRCALPHA)
    text_surface.fill((0, 0, 0, 0))  # Make surface transparent

    # Blit minutes and seconds text onto the surface
    text_surface.blit(text_minutes, (0, 0))
    text_surface.blit(text_seconds, (text_minutes.get_width() + 20, 20))

    text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2))

    # Check if the countdown is over
    if remaining_time <= 0:
        if not counting_up:
            expired = True
            counting_up = True
            start_ticks = pygame.time.get_ticks()

    # Clear the screen
    window.fill(BLACK)

    # Draw the countdown text
    window.blit(text_surface, text_rect)

    # Draw the buttons
    start_stop_text = font_button.render("Start/Stop", True, WHITE)  # Use font_button for button text
    reset_text = font_button.render("Reset", True, WHITE)  # Use font_button for button text
    add_15_min_text = font_button.render("+15 min", True, WHITE)  # Use font_button for button text
    add_15_sec_text = font_button.render("+15 sec", True, WHITE)  # Use font_button for button text
    pygame.draw.rect(window, GREEN2 if running else RED, start_stop_button_rect)
    pygame.draw.rect(window, GREY, reset_button_rect)
    pygame.draw.rect(window, GREY, add_15_min_button_rect)
    pygame.draw.rect(window, GREY, add_15_sec_button_rect)
    window.blit(start_stop_text, (start_stop_button_rect.x + start_stop_button_rect.width // 2 - start_stop_text.get_width() // 2, start_stop_button_rect.y + start_stop_button_rect.height // 2 - start_stop_text.get_height() // 2))
    window.blit(reset_text, (reset_button_rect.x + reset_button_rect.width // 2 - reset_text.get_width() // 2, reset_button_rect.y + reset_button_rect.height // 2 - reset_text.get_height() // 2))
    window.blit(add_15_min_text, (add_15_min_button_rect.x + add_15_min_button_rect.width // 2 - add_15_min_text.get_width() // 2, add_15_min_button_rect.y + add_15_min_button_rect.height // 2 - add_15_min_text.get_height() // 2))
    window.blit(add_15_sec_text, (add_15_sec_button_rect.x + add_15_sec_button_rect.width // 2 - add_15_sec_text.get_width() // 2, add_15_sec_button_rect.y + add_15_sec_button_rect.height // 2 - add_15_sec_text.get_height() // 2))

    # Draw the checkbox
    pygame.draw.rect(window, WHITE, checkbox_rect, 2)  # Draw checkbox outline
    if server_running:
        pygame.draw.rect(window, GREEN, (checkbox_rect.x + 2, checkbox_rect.y + 2, checkbox_width - 4, checkbox_height - 4))  # Draw filled checkbox
    window.blit(checkbox_label, (checkbox_rect.x + checkbox_width + 10, checkbox_rect.y))

    # Update the display
    pygame.display.update()

    # Update button positions if window is resized
    window_width, window_height = window.get_size()
    update_button_positions(window_width, window_height)

# Quit Pygame
pygame.quit()
