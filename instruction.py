import utils

class Instruction:
    def __init__(self, pattern: str, handler):
        self.pattern = pattern
        self.handler = handler

    def execute(self, instr: str):
        args = utils.parse_instruction_args(self.pattern, instr)
        if args is None:
            return False
        self.handler(*args)
        return True

class InstructionExecutor:
    def __init__(self, emulator, renderer):
        self.emulator = emulator
        self.renderer = renderer
        self.instruction_set = [
            Instruction('00E0', self.exec_00E0),
            Instruction('1nnn', self.exec_1nnn),
            Instruction('6xkk', self.exec_6xkk),
            Instruction('7xkk', self.exec_7xkk),
            Instruction('Annn', self.exec_Annn),
            Instruction('Dxyn', self.exec_Dxyn),
        ]

    def execute(self, call_string: str):
        for instruction_exec in self.instruction_set:
            if instruction_exec.execute(call_string):
                return
        self.renderer.put_message(f'Instruction {call_string} not known')

    def exec_00E0(self):
        self.renderer.clear_screen()
        self.renderer.put_message('Clear the screen')

    def exec_1nnn(self, value: int):
        self.emulator.program_counter = value
        self.renderer.put_message(f'Jump to address {value}')

    def exec_6xkk(self, register: int, value: int):
        self.emulator.set_v_register(register, value)
        self.renderer.put_message(f'Set register V{register} to {value}')

    def exec_7xkk(self, register: int, value: int):
        self.emulator.set_v_register(register, self.emulator.v_registers[register] + value)
        self.renderer.put_message(f'Add {value} to register V{register}')

    def exec_Annn(self, value: int):
        self.emulator.set_index_register(value)
        self.renderer.put_message(f'Set register I to {value}')

    def exec_Dxyn(self, x_register: int, y_register: int, n: int):
        self.emulator.draw_bytes(
            self.emulator.v_registers[x_register],
            self.emulator.v_registers[y_register],
            n)
        self.renderer.put_message(f'Draw {n} bytes at (V{x_register}, V{y_register})')
