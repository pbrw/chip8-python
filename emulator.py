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
        self.stack = []
        self.memory = [0] * config.MEMORY_SIZE_KB * 1024
        self.program_counter = config.PROGRAM_START_LOCATION
        self.v_registers = [0] * config.V_REGISTERS_NUMBER
        self.index_register = 0
        self.instruction_executor = InstructionExecutor(self, self.renderer)
        self.timer_register = 0

    def run(self):
        self.load_hex_digit_sprites_to_memory()
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
        self.v_registers[register] = value & 0xFF

    def get_v_register(self, register: int) -> int:
        return self.v_registers[register]

    def set_vf_register(self, value: int):
        self.v_registers[0xF] = value & 0xFF

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

    def load_registers_from_memory(self, n: int):
        begin = self.index_register
        end = begin + n + 1
        for index, value in enumerate(self.memory[begin:end]):
            self.set_v_register(index, value)
        self.set_index_register(end)

    def store_registers_to_memory(self, n: int):
        for index, value in enumerate(self.v_registers[:n + 1]):
            self.memory[self.index_register + index] = value
        self.set_index_register(self.index_register + n + 1)

    def stack_push(self, value: int):
        self.stack.append(value)

    def stack_pop(self) -> int:
        return self.stack.pop()

    def get_delay_timer(self) -> int:
        return self.timer_register

    def set_delay_timer(self, value: int):
        self.timer_register = value & 0xFF

    def load_hex_digit_sprites_to_memory(self):
        data = ['F0909090F0', '2060202070', 'F010F080F0', 'F010F010F0', '9090F01010', 'F080F010F0', 'F080F090F0', 'F010204040', 'F090F090F0', 'F090F010F0']
        for index, byte in enumerate(data):
            self.memory[index * 5: index * 5 + 5] = bytearray.fromhex(byte)