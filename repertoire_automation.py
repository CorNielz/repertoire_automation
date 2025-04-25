from Configs import automation

from Models.game_interface import GameInterface
from Models.threads import ProcessesManager
from Models.key import Key

import time
from threading import Event

class RepertoireAutomation:
    _game_off = Event()
    _game_interface = GameInterface()

    _is_autoplay_on = False

    def run():
        while True:
            if not RepertoireAutomation._game_interface.is_game_on_screen():
                RepertoireAutomation._is_autoplay_on = False
                continue
        
            if not RepertoireAutomation._is_autoplay_on:
                RepertoireAutomation._is_autoplay_on = True
                RepertoireAutomation.autoplay()

            time.sleep(1)
    
    def autoplay():
        for game_key in RepertoireAutomation._game_interface.keys:
            ProcessesManager.send_work(RepertoireAutomation.process_key, game_key)

    def process_key(key: Key) -> None:
        while True:            
            note_type = key.get_note_in_key()
            
            if note_type == "None":
                time.sleep(0.05)
                continue

            elif note_type == "Press":
                key.press()
            elif note_type == "Hold":
                key.hold()   

            time.sleep(0.05)        


if __name__ == "__main__":
    RepertoireAutomation.run()