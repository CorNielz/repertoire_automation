from dataclasses import dataclass
from dataclasses import field
from typing import Protocol
import pyautogui

from Enums.keyboard_action import KeyboardAction

class GetNoteAction(Protocol):
    def fetch_note_action(self) -> KeyboardAction:
        pass

class ColorBasedActionFetcher():
    def fetch_note_action(self, color):
        from Constants.color import PRESS_COLOR_RANGE, HOLD_COLOR_RANGE

        if color[0] in PRESS_COLOR_RANGE[0] and color[1] in PRESS_COLOR_RANGE[1] and color[2] in PRESS_COLOR_RANGE[2]:
            return KeyboardAction.PRESS
        elif color[0] in HOLD_COLOR_RANGE[0] and color[1] in HOLD_COLOR_RANGE[1] and color[2] in HOLD_COLOR_RANGE[2]:
            return KeyboardAction.HOLD
        
        return KeyboardAction.NONE
    
@dataclass
class Key:
    x_position: int = field(default = 0)
    y_position: int = field(default = 0)
    height: int = field(default = 0)
    width: int = field(default = 0)

    keyboard_key: str = field(default = "")
    is_key_hold: bool = field(default = False)

    action_fetcher: GetNoteAction

    def verify_note_type_in_key(self) -> str:
        key_range_screenshot = pyautogui.screenshot(region=self.region())

        for x in range(0, self.width, 10):
            for y in range(0, self.height, 10):
                note = self.action_fetcher.fetch_note_action(key_range_screenshot.getpixel((x, y)))

                if note != KeyboardAction.NONE:
                    return note
        
        return KeyboardAction.NONE
    
    def region(self):
        return (self.x_position, self.y_position, self.width, self.height)