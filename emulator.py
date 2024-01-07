import ui
import clock
import utils
import config

class Emulator:
    def __init__(self):
        self.t_start_ms = -1
        self.executed_cycles = 0
        self.renderer = ui.UiRenderer(self)
        self.clock = clock.Clock(self, self.renderer)
        self.memory = [0] * config.MEMORY_SIZE_KB * 1024
        self.program_counter = config.PROGRAM_START_LOCATION

    def run(self):
        self.t_start_ms = utils.get_current_time_ms()
        self.clock.start()

    def load_program_to_memory(self, code: [int]):
        for index, byte in enumerate(code):
            self.memory[config.PROGRAM_START_LOCATION + index] = byte

    def execute_cycle(self):
        self.executed_cycles += 1

    def get_running_time_ms(self) -> int:
        return utils.get_current_time_ms() - self.t_start_ms

    def get_memory_window(self, size: int) -> [int]:
        begin = self.program_counter
        end = begin + size
        return self.memory[begin:end]
