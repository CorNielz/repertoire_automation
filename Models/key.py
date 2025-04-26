from dataclasses import dataclass
from dataclasses import field

import pyautogui

from Constants.color import PRESS_COLOR_RANGE, HOLD_COLOR_RANGE
from Constants.cooldown import KEY_PRESS_INTERVAL
from Constants.interface import KEY_COLOR

from Enums.keyboard_action import KeyboardAction

@dataclass
class Key:
    x_position: int = field(default = 0)
    y_position: int = field(default = 0)
    height: int = field(default = 0)
    width: int = field(default = 0)

    keyboard_key: str = field(default = "")
    is_key_hold: bool = field(default = False)

    color: tuple[int, int, int] = field(default_factory = lambda: KEY_COLOR)

    is_note_active: bool = field(default = False)
    
    def get_note_in_key(self) -> str:
        key_range_screenshot = pyautogui.screenshot(region=self.region())

        for x in range(0, self.width, 10):
            for y in range(0, self.height, 10):
                note = self.match_note_color(key_range_screenshot.getpixel((x, y)))

                if note != KeyboardAction.NONE:
                    return note
        
        return KeyboardAction.NONE
  
    def match_note_color(self, color):
        if color[0] in PRESS_COLOR_RANGE[0] and color[1] in PRESS_COLOR_RANGE[1] and color[2] in PRESS_COLOR_RANGE[2]:
            return KeyboardAction.PRESS
        elif color[0] in HOLD_COLOR_RANGE[0] and color[1] in HOLD_COLOR_RANGE[1] and color[2] in HOLD_COLOR_RANGE[2]:
            return KeyboardAction.HOLD
        
        return KeyboardAction.NONE 

    def press(self) -> None:
        if self.is_note_active:
            return 
        
        pyautogui.press(self.keyboard_key, interval=KEY_PRESS_INTERVAL)

    def hold(self):
        pyautogui.keyDown(self.keyboard_key)
        self.is_key_hold = True

    def release(self):
        pyautogui.keyUp(self.keyboard_key)
        self.is_key_hold = False

    def region(self):
        return (self.x_position, self.y_position, self.width, self.height)