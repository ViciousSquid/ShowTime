from .timer import Timer
from .constants import TIMERS

class TimerManager:
    def __init__(self, timer_configs):
        self.timers = [Timer(timer_config['length'], timer_config['name']) for timer_config in timer_configs]

    def update_timers(self):
        for timer in self.timers:
            timer.update()