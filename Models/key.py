from dataclasses import dataclass
from dataclasses import field
from typing import Protocol
import mss
import pyautogui
from PIL import Image
import time

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
    action_fetcher: GetNoteAction

    x_position: int = field(default = 0)
    y_position: int = field(default = 0)
    height: int = field(default = 0)
    width: int = field(default = 0)

    keyboard_key: str = field(default = "")
    is_key_hold: bool = field(default = False)

    def verify_note_type_in_key(self) -> str:
        with mss.mss() as sct:
            sct_img = sct.grab(self.monitor())
            key_range_screenshot = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

        color = key_range_screenshot.getpixel(self.center())
        note = self.action_fetcher.fetch_note_action(color)

        if note != KeyboardAction.NONE:
            print(f"Note detected: {time.time()}")

        return note
    
    def region(self):
        return (self.x_position, self.y_position, self.width, self.height)
    
    def center(self):
        return (self.width // 2, self.height // 2)
    
    def monitor(self):
        return {
                "left": self.x_position,
                "top": self.y_position,
                "width": self.width,
                "height": self.height
            }