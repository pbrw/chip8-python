from keypad import Keypad
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
        self.keypad = Keypad()
        self.instruction_set = [
            Instruction('00E0', self.exec_00E0),
            Instruction('00EE', self.exec_00EE),
            Instruction('1nnn', self.exec_1nnn),
            Instruction('2nnn', self.exec_2nnn),
            Instruction('3xkk', self.exec_3xkk),
            Instruction('4xkk', self.exec_4xkk),
            Instruction('5xy0', self.exec_5xy0),
            Instruction('6xkk', self.exec_6xkk),
            Instruction('7xkk', self.exec_7xkk),
            Instruction('8xy0', self.exec_8xy0),
            Instruction('8xy1', self.exec_8xy1),
            Instruction('8xy2', self.exec_8xy2),
            Instruction('8xy3', self.exec_8xy3),
            Instruction('8xy4', self.exec_8xy4),
            Instruction('8xy5', self.exec_8xy5),
            Instruction('8xy6', self.exec_8xy6),
            Instruction('8xy7', self.exec_8xy7),
            Instruction('8xyE', self.exec_8xyE),
            Instruction('9xy0', self.exec_9xy0),
            Instruction('Annn', self.exec_Annn),
            Instruction('Dxyn', self.exec_Dxyn),
            Instruction('Ex9E', self.exec_Ex9E),
            Instruction('ExA1', self.exec_ExA1),
            Instruction('Fx07', self.exec_Fx07),
            Instruction('Fx0A', self.exec_Fx0A),
            Instruction('Fx15', self.exec_Fx15),
            Instruction('Fx1E', self.exec_Fx1E),
            Instruction('Fx33', self.exec_Fx33),
            Instruction('Fx55', self.exec_Fx55),
            Instruction('Fx65', self.exec_Fx65),
        ]

    def execute(self, call_string: str):
        for instruction_exec in self.instruction_set:
            if instruction_exec.execute(call_string):
                return
        self.renderer.put_message(f'Instruction {call_string} not known')

    def exec_00E0(self):
        self.renderer.clear_screen()
        self.renderer.put_message('Clear the screen')

    def exec_00EE(self):
        self.emulator.program_counter = self.emulator.stack_pop()
        self.renderer.put_message('Return from subroutine')

    def exec_1nnn(self, value: int):
        self.emulator.program_counter = value
        self.renderer.put_message(f'Jump to address {value}')

    def exec_2nnn(self, value: int):
        self.emulator.stack_push(self.emulator.program_counter)
        self.emulator.program_counter = value
        self.renderer.put_message(f'Call subroutine at {value}')

    def exec_3xkk(self, x: int, kk: int):
        if self.emulator.v_registers[x] == kk:
            self.emulator.move_program_counter(2)
        self.renderer.put_message(f'If V{x} == {kk}, skip next instruction')

    def exec_4xkk(self, x: int, kk: int):
        if self.emulator.v_registers[x] != kk:
            self.emulator.move_program_counter(2)
        self.renderer.put_message(f'If V{x} != {kk}, skip next instruction')

    def exec_5xy0(self, x: int, y: int):
        if self.emulator.v_registers[x] == self.emulator.v_registers[y]:
            self.emulator.move_program_counter(2)
        self.renderer.put_message(f'If V{x} == V{y}, skip next instruction')

    def exec_6xkk(self, x: int, kk: int):
        self.emulator.set_v_register(x, kk)
        self.renderer.put_message(f'Set register V{x} to {kk}')

    def exec_7xkk(self, x: int, kk: int):
        self.emulator.set_v_register(x, self.emulator.v_registers[x] + kk)
        self.renderer.put_message(f'Add {kk} to register V{x}')

    def exec_8xy0(self, x: int, y: int):
        self.emulator.set_v_register(x, self.emulator.v_registers[y])
        self.renderer.put_message(f'Set register V{x} to V{y}')

    def exec_8xy1(self, x: int, y: int):
        self.emulator.set_v_register(x,
            self.emulator.v_registers[x] | self.emulator.v_registers[y])
        self.renderer.put_message(f'Set register V{x} to V{x} | V{y}')

    def exec_8xy2(self, x: int, y: int):
        self.emulator.set_v_register(x,
            self.emulator.v_registers[x] & self.emulator.v_registers[y])
        self.renderer.put_message(f'Set register V{x} to V{x} & V{y}')

    def exec_8xy3(self, x: int, y: int):
        self.emulator.set_v_register(x,
            self.emulator.v_registers[x] ^ self.emulator.v_registers[y])
        self.renderer.put_message(f'Set register V{x} to V{x} ^ V{y}')

    def exec_8xy4(self, x: int, y: int):
        res = self.emulator.v_registers[x] + self.emulator.v_registers[y]
        self.emulator.set_v_register(x, res)
        if res > 0xFF:
            self.emulator.set_vf_register(1)
        else:
            self.emulator.set_vf_register(0)
        self.renderer.put_message(f'Set register V{x} to V{x} + V{y}')

    def exec_8xy5(self, x: int, y: int):
        res = self.emulator.v_registers[x] - self.emulator.v_registers[y]
        self.emulator.set_v_register(x, res)
        if res < 0:
            res += 0x100
            self.emulator.set_vf_register(0)
        else:
            self.emulator.set_vf_register(1)

        self.renderer.put_message(f'Set register V{x} to V{x} - V{y}')

    def exec_8xy6(self, x: int, _y: int):
        val = self.emulator.v_registers[x]
        self.emulator.set_v_register(x, val >> 1)
        self.emulator.set_vf_register(val & 0x1)
        self.renderer.put_message(f'Set register V{x} to V{x} >> 1')

    def exec_8xy7(self, x: int, y: int):
        res = self.emulator.v_registers[y] - self.emulator.v_registers[x]
        self.emulator.set_v_register(x, res)
        if res < 0:
            res += 0x100
            self.emulator.set_vf_register(0)
        else:
            self.emulator.set_vf_register(1)

        self.renderer.put_message(f'Set register V{x} to V{y} - V{x}')

    def exec_8xyE(self, x: int, _y: int):
        val = self.emulator.v_registers[x]
        self.emulator.set_v_register(x, val << 1)
        if val & (1 << 7):
            self.emulator.set_vf_register(1)
        else:
            self.emulator.set_vf_register(0)
        self.renderer.put_message(f'Set register V{x} to V{x} << 1')

    def exec_9xy0(self, x: int, y: int):
        if self.emulator.v_registers[x] != self.emulator.v_registers[y]:
            self.emulator.move_program_counter(2)
        self.renderer.put_message(f'If V{x} != V{y}, skip next instruction')

    def exec_Annn(self, nnn: int):
        self.emulator.set_index_register(nnn)
        self.renderer.put_message(f'Set register I to {nnn}')

    def exec_Dxyn(self, x: int, y: int, n: int):
        self.emulator.draw_bytes(
            self.emulator.v_registers[x],
            self.emulator.v_registers[y],
            n)
        self.renderer.put_message(f'Draw {n} bytes at (V{x}, V{y})')

    def exec_Ex9E(self, x: int):
        if self.keypad.is_pressed(self.emulator.v_registers[x]):
            self.emulator.move_program_counter(2)
        self.renderer.put_message(f'If key V{x} is pressed, skip next instruction')

    def exec_ExA1(self, x: int):
        if not self.keypad.is_pressed(self.emulator.v_registers[x]):
            self.emulator.move_program_counter(2)
        self.renderer.put_message(f'If key V{x} is not pressed, skip next instruction')

    def exec_Fx07(self, x: int):
        self.emulator.set_v_register(x, self.emulator.timer_register)
        self.renderer.put_message(f'Set register V{x} to delay timer')

    def exec_Fx0A(self, x: int):
        key = self.keypad.get_pressed_released_key_val()
        if key is not None:
            self.emulator.set_v_register(x, key)
        else:
            self.emulator.move_program_counter(-2)
        self.renderer.put_message(f'Wait for key press and store in V{x}')

    def exec_Fx15(self, x: int):
        self.emulator.set_delay_timer(self.emulator.v_registers[x])
        self.renderer.put_message(f'Set delay timer to V{x}')

    def exec_Fx1E(self, x: int):
        self.emulator.set_index_register(self.emulator.get_index_register() + self.emulator.v_registers[x])
        self.renderer.put_message(f'Set register I to I + V{x}')

    def exec_Fx33(self, x: int):
        value = self.emulator.v_registers[x] % 1000
        self.emulator.memory[self.emulator.get_index_register()] = int(value / 100)
        self.emulator.memory[self.emulator.get_index_register() + 1] = int((value % 100) / 10)
        self.emulator.memory[self.emulator.get_index_register() + 2] = int(value % 10)
        self.renderer.put_message(f'Store BCD representation of V{x} in memory')

    def exec_Fx55(self, x: int):
        self.emulator.store_registers_to_memory(x)
        self.renderer.put_message(f'Store registers V0 to V{x} in memory')

    def exec_Fx65(self, x: int):
        self.emulator.load_registers_from_memory(x)
        self.renderer.put_message(f'Load registers V0 to V{x} from memory')
