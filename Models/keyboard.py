from dataclasses import dataclass
from dataclasses import field

import pyautogui

from Constants.cooldown import KEY_PRESS_INTERVAL

@dataclass
class Keyboard:
    keys_held: list[str] = field(default_factory = list)

    def press(self, keyboard_key: str) -> None:        
        pyautogui.press(keyboard_key, interval=KEY_PRESS_INTERVAL)

    def hold(self, keyboard_key: str):
        pyautogui.keyDown(keyboard_key)
        self.keys_held.append(keyboard_key)

    def release(self, keyboard_key):
        pyautogui.keyUp(keyboard_key)
        self.keys_held.remove(keyboard_key)