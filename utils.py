import time


def get_current_time_ms() -> int:
    return time.time_ns() / 1_000_000

def leading_zeros(number: int, expected_len) -> str:
    return str(number).zfill(expected_len)

def byte_to_human(byte: int) -> str:
    if byte < 16:
        return f'0{str(hex(byte)[-1]).upper()}'
    return (hex(byte)[-2:]).upper()