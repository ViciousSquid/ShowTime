import http.server
import socketserver
import threading
import pygame
from constants import *

server_running = False
counter_value = ""

class CounterHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/timer':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(f"Timer: {counter_value}", "utf-8"))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ShowTime remote</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .timer {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            text-align: center;
        }}
        .timer h1 {{
            font-size: 48px;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="timer">
        <h1 id="timer-display">Timer: {counter_value}</h1>
    </div>
    <script>
        function updateTimer() {{
            fetch('/timer')
                .then(response => response.text())
                .then(data => {{
                    document.getElementById('timer-display').textContent = data;
                }})
                .catch(error => console.error('Error fetching timer value:', error));
        }}

        setInterval(updateTimer, 1000);
    </script>
</body>
</html>
            """
            self.wfile.write(bytes(html, "utf-8"))

def update_counter_value(timer):
    global counter_value
    while server_running:
        if timer.running:
            remaining_time = max(timer.countdown - (pygame.time.get_ticks() - timer.start_ticks - timer.paused_time) // 1000, 0)
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            counter_value = f"{minutes:02d}:{seconds:02d}"
            pygame.time.wait(1000)
        else:
            pygame.time.wait(100)  # Wait for a short time to reduce CPU usage

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