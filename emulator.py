import ui
import clock
import utils
import config
from instruction import InstructionExecutor

class Emulator:
    def __init__(self):
        self.t_start_ms = -1
        self.executed_cycles = 0
        self.renderer = ui.UiRenderer(self)
        self.clock = clock.Clock(self, self.renderer)
        self.memory = [0] * config.MEMORY_SIZE_KB * 1024
        self.program_counter = config.PROGRAM_START_LOCATION
        self.v_registers = [0] * config.V_REGISTERS_NUMBER
        self.index_register = 0
        self.instruction_executor = InstructionExecutor(self, self.renderer)

    def run(self):
        self.t_start_ms = utils.get_current_time_ms()
        self.clock.start()

    def load_program_to_memory(self, code: [int]):
        for index, byte in enumerate(code):
            self.memory[config.PROGRAM_START_LOCATION + index] = byte

    def execute_cycle(self):
        self.executed_cycles += 1
        instr = self.fetch_instruction_human_readable()
        self.move_program_counter(2)
        self.instruction_executor.execute(instr)

    def draw_bytes(self, x: int, y: int, n: int):
        begin = self.index_register
        self.renderer.xor_screen(x, y, self.memory[begin: begin + n])

    def move_program_counter(self, n):
        self.program_counter += n

    def fetch_instruction_human_readable(self) -> str:
        first_byte = self.memory[self.program_counter]
        second_byte = self.memory[self.program_counter + 1]
        return utils.byte_to_human(first_byte) + utils.byte_to_human(second_byte)

    def set_v_register(self, register: int, value: int):
        self.v_registers[register] = value

    def get_v_register(self, register: int) -> int:
        return self.v_registers[register]

    def set_vf_register(self, value: int):
        self.v_registers[0xF] = value

    def set_index_register(self, value: int):
        self.index_register = value

    def get_index_register(self) -> int:
        return self.index_register

    def get_running_time_ms(self) -> int:
        return utils.get_current_time_ms() - self.t_start_ms

    def get_memory_window(self, size: int) -> [int]:
        begin = self.program_counter
        end = begin + size
        return self.memory[begin:end]
