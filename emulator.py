import time
import ui
import clock
import utils

class Emulator:
    def __init__(self):
        self.t_start_ms = -1
        self.executed_cycles = 0
        self.renderer = ui.UiRenderer(self)
        self.clock = clock.Clock(self, self.renderer)

    def run(self):
        self.t_start_ms = utils.get_current_time_ms()
        self.clock.start()

    def execute_cycle(self):
        self.executed_cycles += 1

    def get_running_time_ms(self) -> int:
        return self.get_current_time_ms() - self.t_start_ms

    def get_current_time_ms(self) -> int:
        return time.time_ns() / 1_000_000