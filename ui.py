import os

class UiRenderer:
    def __init__(self, emulator):
        self.executed_ui_updates = 0
        self.emulator = emulator

    def update_ui(self, executed_cycles):
        t_running = self.emulator.get_running_time_ms()
        self.clear_console()
        self.render_ui(t_running, executed_cycles)
        self.executed_ui_updates += 1

    def render_ui(self, running_time, executed_cycles):
        print('📺 CHIP-8 Emulator 📺\n----------------------\n')
        print(f'Running: {running_time / 1000:.3f}')
        print(f'Cycle: {executed_cycles + 1}')

    def clear_console(self):
        os.system('clear')
