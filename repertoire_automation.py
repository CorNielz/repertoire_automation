from Models.keyboard import Keyboard
from Models.game_interface import GameInterface
from Models.key import Key

import time

class RepertoireAutomation:
    _keyboard = Keyboard()
    _game_interface = GameInterface()

    def autoplay():
        while True:
            if not RepertoireAutomation._game_interface.is_game_on_screen():
                time.sleep(0.1)
                continue

            for key in RepertoireAutomation._game_interface.keys:
                RepertoireAutomation.process_key(key)
            
    def process_key(key: Key) -> None:
        if key.is_note_in_key():
            key.press()
            

if __name__ == "__main__":
    RepertoireAutomation.autoplay()