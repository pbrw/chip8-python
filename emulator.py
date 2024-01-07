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
        self.v_registers = [0] * config.V_REGISTERS_NUMBER
        self.index_register = 0

    def run(self):
        self.t_start_ms = utils.get_current_time_ms()
        self.clock.start()

    def load_program_to_memory(self, code: [int]):
        for index, byte in enumerate(code):
            self.memory[config.PROGRAM_START_LOCATION + index] = byte

    def execute_cycle(self):
        self.executed_cycles += 1
        instr = self.fetch_instruction_human_readable()
        self.execute_instruction(instr)
        self.move_program_counter()

    def execute_instruction(self, instr: int):
        if instr[0] == '6':
            register = int(instr[1], 16)
            value = int(instr[2:], 16)
            self.set_v_register(register, value)
            self.renderer.put_message(f'Set register V{register} to {value}')
        elif instr[0] == 'A':
            value = int(instr[1:], 16)
            self.set_index_register(value)
            self.renderer.put_message(f'Set register I to {value}')
        elif instr == '00E0':
            self.renderer.put_message('Clear the screen')
        elif instr[0] == 'D':
            x_register = int(instr[1], 16)
            y_register = int(instr[2], 16)
            n = int(instr[3 ], 16)
            self.renderer.put_message(f'Draw {n} bytes at (V{x_register}, V{y_register})')
        elif instr[0] == '1':
            value = int(instr[1:], 16)
            self.renderer.put_message(f'Jump to address {value}')
        else:
            self.renderer.put_message(f'Instruction {instr} not known')

    def move_program_counter(self):
        self.program_counter += 2

    def fetch_instruction_human_readable(self) -> str:
        first_byte = self.memory[self.program_counter]
        second_byte = self.memory[self.program_counter + 1]
        return utils.byte_to_human(first_byte) + utils.byte_to_human(second_byte)

    def set_v_register(self, register: int, value: int):
        self.v_registers[register] = value

    def get_v_register(self, register: int) -> int:
        return self.v_registers[register]

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