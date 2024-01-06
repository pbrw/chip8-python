import emulator as emul

PROGRAM_CODE = [
    '6007', # Sets V0 to 7
    'A859', # Sets I to 2137
    '00E0', # Clear screen
    'D3B5', # Draw 5 bytes at (V3, V11)
    '1800', # Jump to adress 2048
    '5001', # Not an instruction
]

def main():
    print("Starting CHIP-8 Emulator")
    emulator = emul.Emulator()
    emulator.run()

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
