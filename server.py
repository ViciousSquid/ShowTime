import http.server
import socketserver
import threading
import pygame
from constants import *

server_running = False
counter_value = ""

class CounterHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(f"<html><body><h1>Timer: {counter_value}</h1></body></html>", "utf-8"))

def update_counter_value(timer):
    global counter_value
    while server_running:
        remaining_time = max(timer.countdown - (pygame.time.get_ticks() - timer.start_ticks - timer.paused_time) // 1000, 0)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        counter_value = f"{minutes:02d}:{seconds:02d}"
        pygame.time.wait(1000)

def start_server(timer):
    global server_running
    server_running = True
    print("LOG: HTTP server running on localhost:8000")
    server = socketserver.TCPServer(("", 8000), CounterHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    counter_thread = threading.Thread(target=update_counter_value, args=(timer,))
    counter_thread.start()

def stop_server():
    global server_running
    server_running = False