import json

with open('data/config.json') as f:
    config = json.load(f)
    TIMERS = config['timers']

# Window settings
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

# Colours
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (147, 197, 114)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 191, 0)
GREY = (40, 40, 43)

# Button settings
BUTTON_WIDTH = 160
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

# Checkbox settings
CHECKBOX_WIDTH = 25
CHECKBOX_HEIGHT = 25