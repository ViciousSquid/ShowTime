# change is the only real constant in life

import json

# Load constants from config.json
with open('config.json') as f:
    config = json.load(f)

# Window settings
WINDOW_WIDTH = config['window']['width']
WINDOW_HEIGHT = config['window']['height']

# Countdown settings
INITIAL_COUNTDOWN = config['countdown']['initial']

# Colors
BLACK = tuple(config['colors']['black'])
GREEN = tuple(config['colors']['green'])
GREEN2 = tuple(config['colors']['green2'])
RED = tuple(config['colors']['red'])
WHITE = tuple(config['colors']['white'])
YELLOW = tuple(config['colors']['yellow'])
GREY = tuple(config['colors']['grey'])

# Button settings
BUTTON_WIDTH = config['button']['width']
BUTTON_HEIGHT = config['button']['height']
BUTTON_SPACING = config['button']['spacing']

# Checkbox settings
CHECKBOX_WIDTH = config['checkbox']['width']
CHECKBOX_HEIGHT = config['checkbox']['height']

# Timer settings
TIMERS = config['timers']