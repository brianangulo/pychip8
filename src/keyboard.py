from typing import Sequence
import pygame


class Keyboard:
    """
    keyboard mapper
    """

    def __init__(self, _pygame: pygame) -> None:
        self.key_map = {
            _pygame.K_0: 0x00,
            _pygame.K_1: 0x01,
            _pygame.K_2: 0x02,
            _pygame.K_3: 0x03,
            _pygame.K_4: 0x04,
            _pygame.K_5: 0x05,
            _pygame.K_6: 0x06,
            _pygame.K_7: 0x07,
            _pygame.K_8: 0x08,
            _pygame.K_9: 0x09,
            _pygame.K_a: 0x0a,
            _pygame.K_b: 0x0b,
            _pygame.K_c: 0x0c,
            _pygame.K_d: 0x0d,
            _pygame.K_e: 0x0e,
            _pygame.K_f: 0x0f,
        }
        self.keys_pressed = []
        self.event_callback = None

    def set_pressed(self, keyboard_state: Sequence[bool]) -> 'list[int]':
        """Sets the state for currently pressed keys. This must be run on the render loop"""
        # first we clear current state
        self.keys_pressed.clear()
        for key in self.key_map:
            if keyboard_state[key]:
                # when the cpu awaits for next key press
                if self.event_callback:
                    self.event_callback(self.key_map[key])
                # add to pressed keys
                self.keys_pressed.append(self.key_map[key])
        return self.keys_pressed

    def is_key_pressed(self, key: int):
        return key in self.keys_pressed
    
    def set_event_callback(self, cb):
        # the callback should take key pressed as arg
        self.event_callback = cb
    