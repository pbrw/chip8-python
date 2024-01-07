import os
import config
import utils

class UiRenderer:
    def __init__(self, emulator):
        self.executed_ui_updates = 0
        self.emulator = emulator

    def update_ui(self):
        self.clear_console()
        self.render_ui(
            self.emulator.get_running_time_ms(),
            self.emulator.executed_cycles
        )
        self.executed_ui_updates += 1

    def render_ui(self, running_time, executed_cycles):
        print('📺 CHIP-8 Emulator 📺\n----------------------\n')
        print(f'Running: {running_time / 1000:.3f}')
        print(f'Cycle: {executed_cycles + 1}')
        print('')
        self.render_memory()

    def render_memory(self):
        memory = self.emulator.get_memory_window(config.UI_MEMORY_WINDOW_SIZE)
        current_location = self.emulator.program_counter
        print('Memory:')
        for index, byte in enumerate(memory):
            print(f'\t{utils.leading_zeros(current_location + index, 4)}: {utils.byte_to_human(byte)}')


    def clear_console(self):
        os.system('clear')
