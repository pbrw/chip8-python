import math
import time
import config

class Clock:
    def __init__(self, emulator, renderer):
        self.emulator = emulator
        self.renderer = renderer
        self.executed_delay_timer_ticks = 0

    def start(self):
        while True:
            running_time = self.emulator.get_running_time_ms()

            expected_executed_cycles = self.calculate_exptected_events(running_time, config.CLOCK_SPEED_HZ)
            while expected_executed_cycles > self.emulator.executed_cycles:
                self.emulator.execute_cycle()

            expected_executed_ui_updates = self.calculate_exptected_events(running_time, config.UPDATE_UI_SPEED_HZ)
            while expected_executed_ui_updates > self.renderer.executed_ui_updates:
                self.renderer.update_ui()

            expected_executed_delay_timer_ticks = self.calculate_exptected_events(running_time, config.DELAY_TIMER_SPEED_HZ)
            while expected_executed_delay_timer_ticks > self.executed_delay_timer_ticks:
                self.delay_timer_tick()

            time.sleep(1 / config.LOOP_SPEED_HZ)

    def delay_timer_tick(self):
        self.executed_delay_timer_ticks += 1
        delay_timer = self.emulator.get_delay_timer()
        if delay_timer > 0:
            self.emulator.set_delay_timer(delay_timer - 1)

    def calculate_exptected_events(self, running_time_ms, event_speed_hz):
        return math.floor(running_time_ms * event_speed_hz / 1000)