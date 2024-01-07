import emulator as emul

PROGRAM_CODE = [
    '600A', # Sets V0 to 7
    'A859', # Sets I to 2137
    'D3B5', # Draw 5 bytes at (V3, V11)
    '1800', # Jump to adress 2048
    '00E0', # Clear screen
    '5001', # Not an instruction
]

def main():
    print("Starting CHIP-8 Emulator")
    emulator = emul.Emulator()
    emulator.load_program_to_memory(convert_code_human_to_hex(PROGRAM_CODE))
    emulator.run()

def convert_code_human_to_hex(code: [str]) -> [int]:
    res = []
    for instr in code:
        res.append(int(instr[0:2], 16))
        res.append(int(instr[2:4], 16))
    return res

if __name__ == "__main__":
    main()
