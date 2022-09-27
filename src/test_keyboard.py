from keyboard import Keyboard
from unittest.mock import Mock
import pygame

def test_key_presses_clear_pressed():
    keyboard = Keyboard(pygame)
    test_bool_seq = [True, False, True]
    keyboard.keys_pressed = test_bool_seq
    # this should throw after clearing keys_pressed
    try:
        keyboard.set_pressed([])
    except:
        print("it threw as expected")
        # but it cleared the keys pressed state
    assert len(keyboard.keys_pressed) == 0
    