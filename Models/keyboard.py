import pyautogui

from dataclasses import dataclass
from dataclasses import field

@dataclass(order=True)
class Keyboard:    
    held_keys: dict[str, bool] = field(default_factory=dict[str, bool])

    def press_key(self, key: str):
        if self.held_keys.get(key, False):
            pyautogui.keyDown(key)
            self.held_keys[key] = True

    def release_key(self, key: str):
        if self.held_keys.get(key, True):
            pyautogui.keyUp(key)
            self.held_keys[key] = False

    def release_all_keys(self):
        for key, held in self.held_keys.items():
            if held:
                pyautogui.keyUp(key)

        self.held_keys.clear()