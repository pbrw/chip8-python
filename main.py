import sys
import utils
import emulator as emul
import config

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
    utils.clear_log_file()

    rom_file_path = config.ROM_CODE_FILE_PATH
    if len(sys.argv) > 1:
        rom_file_path = sys.argv[1]

    bytecode = load_file_content_as_bytes(rom_file_path)
    emulator = emul.Emulator()
    emulator.load_program_to_memory(bytecode)
    emulator.run()

def convert_code_human_to_hex(code: [str]) -> [int]:
    res = []
    for instr in code:
        res.append(int(instr[0:2], 16))
        res.append(int(instr[2:4], 16))
    return res

def load_file_content_as_bytes(file_path: str) -> [int]:
    with open(file_path, 'rb') as file:
        return file.read()

if __name__ == "__main__":
    main()
