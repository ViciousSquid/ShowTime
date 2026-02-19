import pygame
import threading
import http.server
import socketserver
import sys
from typing import Tuple, Optional

# ==================== CONFIG ====================
INITIAL_TIME = 900          # 15 minutes
FPS = 60
PORT = 8000

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 220, 0)
RED = (255, 50, 50)
GREY = (45, 45, 50)
LIGHT_GREY = (70, 70, 75)
WHITE = (255, 255, 255)

class Button:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, color: Tuple[int, int, int], hover_color: Optional[Tuple] = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color or color
        self.current_color = color

    def update(self, mouse_pos):
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, LIGHT_GREY, self.rect, width=2, border_radius=8)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class CountdownTimer:
    def __init__(self, initial_seconds: int = INITIAL_TIME):
        self.initial_seconds = initial_seconds
        self.reset()

    def reset(self):
        self.time_left = self.initial_seconds
        self.is_running = False
        self.start_ticks = 0
        self.is_overtime = False
        self.overtime_start = 0

    def toggle(self):
        if self.is_running:
            self.pause()
        else:
            self.resume()

    def pause(self):
        if self.is_running:
            elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
            self.time_left = max(self.time_left - elapsed, 0)
            self.is_running = False

    def resume(self):
        if not self.is_running:
            self.start_ticks = pygame.time.get_ticks()
            self.is_running = True
            if self.time_left <= 0:
                self.is_overtime = True
                self.overtime_start = pygame.time.get_ticks()

    def add_time(self, seconds: int):
        if self.is_running:
            elapsed_so_far = (pygame.time.get_ticks() - self.start_ticks) // 1000
            self.time_left = self.time_left - elapsed_so_far + seconds
            self.start_ticks = pygame.time.get_ticks()  # restart timing
        else:
            self.time_left = max(self.time_left + seconds, 0)

    def get_display_seconds(self) -> Tuple[int, bool]:
        """Returns (total_seconds, is_overtime)"""
        if self.is_running:
            elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
            if not self.is_overtime:
                remaining = self.time_left - elapsed
                if remaining <= 0:
                    self.is_overtime = True
                    self.overtime_start = pygame.time.get_ticks()
                    return 0, True
                return remaining, False
            else:
                overtime = (pygame.time.get_ticks() - self.overtime_start) // 1000
                return overtime, True
        else:
            return max(self.time_left, 0), self.is_overtime


class ShowTimeApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
        pygame.display.set_caption("ShowTime")
        self.clock = pygame.time.Clock()
        self.timer = CountdownTimer()

        self.font_large = None
        self.font_small = None
        self.font_tiny = None

        self.server = None
        self.server_thread = None
        self.server_running = False

        self.fullscreen = False
        self.original_size = (1024, 600)

        self.setup_ui()

    def setup_ui(self):
        self.update_fonts()
        self.update_button_positions()

    def update_fonts(self):
        w, h = self.screen.get_size()
        self.font_large = pygame.font.Font(None, int(h * 0.48))
        self.font_sec = pygame.font.Font(None, int(h * 0.28))
        self.font_small = pygame.font.Font(None, 26)
        self.font_tiny = pygame.font.Font(None, 20)

    def update_button_positions(self):
        w, h = self.screen.get_size()
        btn_w, btn_h = 170, 58
        spacing = 25
        y = h - btn_h - 30

        self.start_btn = Button(40, y, btn_w, btn_h, "START", (0, 180, 0), (0, 220, 0))
        self.reset_btn = Button(40 + btn_w + spacing, y, btn_w, btn_h, "RESET", GREY, LIGHT_GREY)
        self.add_min_btn = Button(40 + 2 * (btn_w + spacing), y, btn_w, btn_h, "+15 MIN", GREY, LIGHT_GREY)
        self.add_sec_btn = Button(40 + 3 * (btn_w + spacing), y, btn_w, btn_h, "+15 SEC", GREY, LIGHT_GREY)

    def make_handler(self):
        timer = self.timer
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                seconds, overtime = timer.get_display_seconds()
                minutes = seconds // 60
                secs = seconds % 60
                status = "OVERTIME" if overtime else ""
                color = "#ff3333" if overtime else "#00ff00"
                html = f"""
                <html><head><meta http-equiv="refresh" content="1"></head>
                <body style="background:#111;color:{color};font-family:monospace;text-align:center;padding-top:80px;">
                    <h1 style="font-size:6em;margin:0;">{minutes:02d}:{secs:02d}</h1>
                    <p style="font-size:1.5em;">{status}</p>
                </body></html>"""
                self.wfile.write(html.encode('utf-8'))
        return Handler

    def toggle_server(self):
        if self.server_running:
            self.stop_server()
        else:
            self.start_server()

    def start_server(self):
        try:
            handler = self.make_handler()
            self.server = socketserver.TCPServer(("", PORT), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            self.server_running = True
            print(f"LOG: HTTP server running → http://localhost:{PORT}")
        except Exception as e:
            print(f"LOG: Server failed to start: {e}")

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        self.server_running = False
        print("LOG: HTTP server stopped")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.cleanup()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                self.update_fonts()
                self.update_button_positions()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.start_btn.rect.collidepoint(pos):
                    self.timer.toggle()
                elif self.reset_btn.rect.collidepoint(pos):
                    self.timer.reset()
                elif self.add_min_btn.rect.collidepoint(pos):
                    self.timer.add_time(900)
                elif self.add_sec_btn.rect.collidepoint(pos):
                    self.timer.add_time(15)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.timer.toggle()
                elif event.key == pygame.K_r:
                    self.timer.reset()
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    self.timer.add_time(15)
                elif event.key == pygame.K_MINUS:
                    self.timer.add_time(-15)
                elif event.key == pygame.K_s:
                    self.toggle_server()
                elif event.key == pygame.K_f:
                    self.toggle_fullscreen()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.original_size, pygame.RESIZABLE)
        self.update_fonts()
        self.update_button_positions()

    def draw(self):
        self.screen.fill(BLACK)
        w, h = self.screen.get_size()

        seconds, is_overtime = self.timer.get_display_seconds()
        minutes = seconds // 60
        secs = seconds % 60

        color = RED if is_overtime else (YELLOW if seconds <= 300 else GREEN)

        min_surf = self.font_large.render(f"{minutes:02d}", True, color)
        sec_surf = self.font_sec.render(f":{secs:02d}", True, color)

        total_w = min_surf.get_width() + sec_surf.get_width()
        x = (w - total_w) // 2
        y = (h - min_surf.get_height()) // 2 - 30

        self.screen.blit(min_surf, (x, y))
        self.screen.blit(sec_surf, (x + min_surf.get_width(), y + min_surf.get_height() - sec_surf.get_height() - 15))

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in (self.start_btn, self.reset_btn, self.add_min_btn, self.add_sec_btn):
            btn.update(mouse_pos)
            btn.draw(self.screen, self.font_small)

        # Status
        status = f"Remote: {'ON' if self.server_running else 'OFF'}  (S to toggle)"
        status_surf = self.font_tiny.render(status, True, WHITE)
        self.screen.blit(status_surf, (35, 28))

        # Help
        help_text = "SPACE = Start/Stop • R = Reset • +/- = ±15s • F = Fullscreen"
        help_surf = self.font_tiny.render(help_text, True, (160, 160, 160))
        self.screen.blit(help_surf, (35, h - 35))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

    def cleanup(self):
        if self.server_running:
            self.stop_server()
        pygame.quit()


if __name__ == "__main__":
    app = ShowTimeApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.cleanup()