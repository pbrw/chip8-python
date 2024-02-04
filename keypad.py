import keyboard

KEYPAD_SIZE = 16

class Keypad:
    def __init__(self):
        self.key_mapping = {
            0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'a',
            11: 'b',
            12: 'c',
            13: 'd',
            14: 'e',
            15: 'f'
        }
        self.pressed_key_cache = None

    def is_pressed(self, val):
        return keyboard.is_pressed(self._val_to_key(val))

    def get_pressed_released_key_val(self):
        if self.pressed_key_cache is not None:
            if not self.is_pressed(self.pressed_key_cache):
                res = self.pressed_key_cache
                self.pressed_key_cache = None
                return res
            return None

        for key in range(KEYPAD_SIZE):
            if self.is_pressed(key):
                self.pressed_key_cache = key
                break

        return None

    def _val_to_key(self, val):
        return self.key_mapping.get(val)