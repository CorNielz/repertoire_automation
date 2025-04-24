import pyautogui
import time

from Models.game_interface import GameInterface

_game_interface = GameInterface()

class InterfaceTests:
    def exhibit_keys_positions():
        for key in _game_interface.keys:
            pyautogui.moveTo(x = key.x_position, y = key.y_position, duration=0.2)

    def test_note_detection():     
        for key in _game_interface.keys:
            pyautogui.moveTo(x = key.x_position, y = key.y_position, duration=0.2)

            if key.is_note_in_key():
                pyautogui.keyDown(key.keyboard_key)
                
pyautogui.FAILSAFE = True

InterfaceTests.exhibit_keys_positions()
InterfaceTests.test_note_detection()

pyautogui.FAILSAFE = False
    