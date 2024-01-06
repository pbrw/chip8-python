import math
import time
import config
import ui


class Emulator:
    def __init__(self):
        self.t_start = -1
        self.executed_cycles = 0
        self.renderer = ui.UiRenderer(self)

    def start(self):
        self.t_start = self.get_current_time_ms()
        while True:
            t_running = self.get_running_time_ms()
            expected_executed_cycles = math.floor(t_running * config.CLOCK_SPEED_HZ / 1000)
            while expected_executed_cycles > self.executed_cycles:
                self.execute_cycle()
            expected_executed_ui_updates = math.floor(t_running * config.UPDATE_UI_SPEED_HZ / 1000) + 1
            while expected_executed_ui_updates > self.renderer.executed_ui_updates:
                self.renderer.update_ui(self.executed_cycles)
            time.sleep(1 / config.LOOP_SPEED_HZ)

    def execute_cycle(self):
        self.executed_cycles += 1

    def get_running_time_ms(self) -> int:
        return self.get_current_time_ms() - self.t_start

    def get_current_time_ms(self) -> int:
        return time.time_ns() / 1_000_000