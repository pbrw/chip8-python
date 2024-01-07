import os
import config
import utils

class UiRenderer:
    def __init__(self, emulator):
        self.executed_ui_updates = 0
        self.emulator = emulator
        self.messages = []
        self.screen = self.get_empty_screen()

    def update_ui(self):
        self.clear_console()
        self.render_ui(
            self.emulator.get_running_time_ms(),
            self.emulator.executed_cycles
        )
        self.executed_ui_updates += 1

    def render_ui(self, running_time, executed_cycles):
        print('📺 CHIP-8 Emulator 📺\n----------------------\n')
        self.render_screen()
        print('')
        print(f'Running: {running_time / 1000:.3f}')
        print(f'Cycle: {executed_cycles + 1}')
        print('')
        self.render_index_register()
        print('')
        self.render_registers()
        print('')
        self.render_memory()
        print('')
        self.render_messages()

    def render_memory(self):
        memory = self.emulator.get_memory_window(config.UI_MEMORY_WINDOW_SIZE)
        current_location = self.emulator.program_counter
        print('Memory:')
        for index, byte in enumerate(memory):
            output = f'\t{utils.leading_zeros(current_location + index, 4)}: {utils.byte_to_human(byte)}'
            if index == 0:
                print(f'{output} <=')
            else:
                print(f'{output}')

    def render_messages(self):
        print('Messages:')
        for message in self.messages[-config.UI_MESSAGES_WINDOW_SIZE:]:
            print(f'\t{message}')

    def render_registers(self):
        print('Registers:')
        for index, register in enumerate(self.emulator.v_registers):
            print(f'\tV{index}: {register}')

    def render_index_register(self):
        print(f'Index register: {self.emulator.index_register}')

    def render_screen(self):
        for index in range(config.SCREEN_HEIGHT):
            print(' ', end='')
            for col in self.screen:
                for i in range(8):
                    if col[index] & (1 << (7 - i)):
                        self.render_black_pixel()
                    else:
                        self.render_white_pixel()
            print()

    def render_black_pixel(self):
        print('  ', end='')

    def render_white_pixel(self):
        print('\u2588', end='')
        print('\u2588', end='')

    def clear_screen(self):
        self.screen =  self.get_empty_screen()

    def get_empty_screen(self):
        return [[0] * config.SCREEN_HEIGHT for _ in range(0, config.SCREEN_WIDTH, 8)]

    def put_message(self, message: str):
        self.messages.append(message)

    def clear_console(self):
        os.system('clear')
