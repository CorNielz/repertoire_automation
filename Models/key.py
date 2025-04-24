from dataclasses import dataclass
from dataclasses import field

import pyautogui

@dataclass
class Key:
    x_position: int = field(default = 0)
    y_position: int = field(default = 0)

    keyboard_key: str = field(default = "")

    color: tuple[int, int, int] = field(default_factory = lambda: (255, 255, 255))


    def is_note_in_key(self):
        if not pyautogui.pixelMatchesColor(self.x_position, self.y_position, self.color, tolerance=30):
            return True
        
        return False