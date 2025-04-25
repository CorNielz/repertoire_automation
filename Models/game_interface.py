from dataclasses import dataclass
from dataclasses import field

import pyautogui

from Constants.interface import KEYS_DATA

from Models.key import Key

@dataclass
class GameInterface:
    screen_width: int = field(default = 0)
    screen_height: int = field(default = 0)

    keys: list[Key] = field(default_factory = list)


    def get_screen_resolution(self) -> None:
        self.screen_width, self.screen_height = pyautogui.size()

    def get_ingame_keys(self) -> None:
        for key_index in KEYS_DATA:
            current_key = Key()

            current_key.x_position = KEYS_DATA[key_index]["X"]
            current_key.y_position = KEYS_DATA[key_index]["Y"]
            current_key.keyboard_key = KEYS_DATA[key_index]["Key"]

            self.keys.append(current_key)

    def is_game_on_screen(self) -> bool:
        for key in self.keys:
            if key.is_key_present_in_interface():
                return True
            
        return False

    def __init__(self):
        self.keys = []

        GameInterface.get_screen_resolution(self)
        GameInterface.get_ingame_keys(self)