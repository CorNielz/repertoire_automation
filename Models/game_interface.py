from dataclasses import dataclass
from dataclasses import field
from typing import Protocol
import pyautogui

from Constants.confidence import KEY_CONFIDENCE
from Constants.image_path import KEY

from Models.key import Key, ColorBasedActionFetcher

class KeyDataLoader(Protocol):
    def load_keys(self) -> list[Key]:
        pass

class ConstantsKeyDataLoader():
    def load_keys(self) -> list[Key]:
        from Constants.interface import KEYS_DATA

        keys = []
        action_fetcher = ColorBasedActionFetcher()
        
        for key_index in KEYS_DATA:
            current_key = Key(
                action_fetcher=action_fetcher,
                x_position = KEYS_DATA[key_index]["X"],
                y_position = KEYS_DATA[key_index]["Y"],
                height = KEYS_DATA[key_index]["Height"],
                width = KEYS_DATA[key_index]["Width"],
                keyboard_key = KEYS_DATA[key_index]["Key"],
            )

            keys.append(current_key)

        return keys

@dataclass
class GameInterface:
    screen_width: int = field(default = 0)
    screen_height: int = field(default = 0)

    keys: list[Key] = field(default_factory = list)

    def update_screen_resolution(self) -> None:
        self.screen_width, self.screen_height = pyautogui.size()

class GameInterfaceDetection:
    def is_game_on_screen(self) -> bool:
        try:
            pyautogui.locateOnScreen(KEY, confidence=KEY_CONFIDENCE)
            return True
        except pyautogui.ImageNotFoundException: 
            return False
        
def build_game_interface(loader: KeyDataLoader) -> GameInterface:
    interface = GameInterface(keys=loader.load_keys())
    interface.update_screen_resolution()

    return interface