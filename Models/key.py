from dataclasses import dataclass
from dataclasses import field

import pyautogui

from Constants.interface import KEY_COLOR
from Constants.cooldown import KEY_PRESS_INTERVAL

@dataclass
class Key:
    x_position: int = field(default = 0)
    y_position: int = field(default = 0)

    keyboard_key: str = field(default = "")
    is_key_hold: bool = field(default = False)

    color: tuple[int, int, int] = field(default_factory = lambda: KEY_COLOR)

    is_note_active: bool = field(default = False)
    
    
    def is_note_in_key(self):
        if not pyautogui.pixelMatchesColor(self.x_position, self.y_position, self.color, tolerance=30):
            return True
        
        return False
    
    def press(self) -> None:
        if self.is_note_active:
            return 
        
        pyautogui.press(self.keyboard_key, interval=KEY_PRESS_INTERVAL)

    def hold(self):
        pyautogui.keyDown(self.keyboard_key)

    def release(self):
        pyautogui.keyUp(self.keyboard_key)