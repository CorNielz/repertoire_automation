from dataclasses import dataclass
from dataclasses import field

import pyautogui

pyautogui.PAUSE = 0

@dataclass
class Key:
    x_position: int = field(default = 0)
    y_position: int = field(default = 0)

    keyboard_key: str = field(default = "")
    is_key_hold: bool = field(default = False)
    color: tuple[int, int, int] = field(default_factory = lambda: (255, 255, 255))


    def is_key_present_in_interface(self):
        if pyautogui.pixelMatchesColor(self.x_position, self.y_position, self.color, tolerance=30):
            return True
        
        return False
    
    def is_note_in_key(self):
        if not pyautogui.pixelMatchesColor(self.x_position, self.y_position, self.color, tolerance=30):
            return True
        
        return False
    
    def press(self) -> None:
        pyautogui.keyDown(self.keyboard_key)
        pyautogui.keyUp(self.keyboard_key)

    def hold(self):
        pyautogui.keyDown(self.keyboard_key)

    def release(self):
        pyautogui.keyUp(self.keyboard_key)