from dataclasses import dataclass
from dataclasses import field
from typing import Protocol
import pyautogui
from mss import mss
import numpy

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
    
class ScreenCapture():
    def __init__(self):
        self._sct = mss()
    
    def capture_region(self, region: dict) -> numpy.ndarray:
        sct_img = self._sct.grab(region)

        return numpy.array(sct_img)
    
@dataclass
class Key:
    action_fetcher: GetNoteAction
    screen_capture: ScreenCapture

    x_position: int = field(default = 0)
    y_position: int = field(default = 0)
    height: int = field(default = 0)
    width: int = field(default = 0)

    keyboard_key: str = field(default = "")
    is_key_hold: bool = field(default = False)

    def verify_note_type_in_key(self) -> KeyboardAction:
        key_range_screenshot = self.screen_capture.capture_region(self.region())

        for x in range(0, self.width, 10):
            for y in range(0, self.height, 10):
                color = key_range_screenshot[y, x][:3]
                note = self.action_fetcher.fetch_note_action(color[::1])

                if note != KeyboardAction.NONE:
                    return note
        
        return KeyboardAction.NONE
    
    def region(self) -> dict[str, int]:
        return {"top": self.y_position, "left": self.x_position, "width": self.width, "height": self.height}