import random
import time
import config

def get_current_time_ms() -> int:
    return time.time_ns() / 1_000_000

def leading_zeros(number: int, expected_len) -> str:
    return str(number).zfill(expected_len)

def byte_to_human(byte: int) -> str:
    if byte < 16:
        return f'0{str(hex(byte)[-1]).upper()}'
    return (hex(byte)[-2:]).upper()

def parse_instruction_args(pattern: str, instr: str) -> [int]:
    if len(pattern) != len(instr):
        return None
    res = []
    cur = 0
    for index, char in enumerate(pattern):
        if char.islower():
            if index != 0 and pattern[index - 1].islower() and pattern[index - 1] != char:
                res.append(cur)
                cur = 0
            cur = cur * 16 + int(instr[index], 16)
        else:
            if char != instr[index]:
                return None
            if index != 0 and pattern[index - 1].islower():
                res.append(cur)
                cur = 0
    if pattern[-1].islower():
        res.append(cur)

    return res

def get_random_byte() -> int:
    return random.randint(0, 0xFF)

def clear_log_file():
    with open(config.LOG_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write('')

def append_message_to_log_file(string: str):
    with open(config.LOG_FILE_PATH, 'a', encoding='utf-8') as file:
        file.write(string)
        file.write('\n')
