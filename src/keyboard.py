class Keyboard:
    """
    keyboard mapper
    """

    def __init__(self) -> None:
        self.key_map = {
            '1': 0x01,
            '2': 0x02,
            '3': 0x03,
            'c': 0x0c,
            '4': 0x04,
            '5': 0x05,
            '6': 0x06,
            'd': 0x0d,
            '7': 0x07,
            '8': 0x08,
            '9': 0x09,
            'e': 0x0e,
            'a': 0x0a,
            '0': 0x00,
            'b': 0x0b,
            'f': 0x0f,
        }
        self.keys_pressed = []

    def keys_bind_events(event):
        print(event.char)
