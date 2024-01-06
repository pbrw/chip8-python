import time


ROM_CODE_FILE_PATH = 'test/hello.ch8'

CLOCK_SPEED_HZ = 10

LOOP_SPEED_HZ = 1000

PROGRAM_CODE = [
    '6007', # Sets V0 to 7
    'A859', # Sets I to 2137
    '00E0', # Clear screen
    'D3B5', # Draw 5 bytes at (V3, V11)
    '1800', # Jump to adress 2048
    '5001', # Not an instruction
]

executed_cycles = 0

def run(clock_speed_hz: int):
    t_start = get_current_time_ms()

    while True:
        t_now = get_current_time_ms()
        t_running = t_now - t_start
        expected_executed_cycles = round(t_running * clock_speed_hz / 1000)
        while expected_executed_cycles > executed_cycles:
            execute_cycle()
        time.sleep(1 / LOOP_SPEED_HZ)

def execute_cycle():
    global executed_cycles
    print(f'Cycle: {executed_cycles + 1}')
    executed_cycles += 1

def get_current_time_ms() -> int:
    return time.time_ns() / 1_000_000

def main():
    print("Starting CHIP-8 Emulator")
    run(CLOCK_SPEED_HZ)

def get_code_human_readable(file_path: str) -> [str]:
    code: [str] = []
    with open(file_path, "rb") as file:
        content: bytes = file.read()
        for index in range(0, len(content), 2):
            first_byte = get_human_readable_byte(content[index])
            second_byte = get_human_readable_byte(content[index + 1])
            code.append(first_byte + second_byte)
    return code

def get_human_readable_byte(byte: any) -> str:
    if int(byte) < 16:
        return f'0{hex(byte)[-1]}'
    return (hex(byte)[-2:]).upper()

def interpret_code(code: [str]):
    for index, instr in enumerate(code):
        print(f'{str(index).zfill(3)} - ', end='')
        interpret_instruction(instr)

def interpret_instruction(instr: str):
    print(f'{instr} - ', end='')
    if instr[0] == '6':
        register = int(instr[1], 16)
        value = int(instr[2:], 16)
        print(f'Set register V{register} to {value}')
    elif instr[0] == 'A':
        value = int(instr[1:], 16)
        print(f'Set register I to {value}')
    elif instr == '00E0':
        print('Clear the screen')
    elif instr[0] == 'D':
        x_register = int(instr[1], 16)
        y_register = int(instr[2], 16)
        n = int(instr[3 ], 16)
        print(f'Draw {n} bytes at (V{x_register}, V{y_register})')
    elif instr[0] == '1':
        value = int(instr[1:], 16)
        print(f'Jump to address {value}')
    else:
        print(f'Instruction {instr} not known')

if __name__ == "__main__":
    main()