from Configs import automation

from Functions.threads import Threads

from Models.game_interface import GameInterface
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
                RepertoireAutomation._game_off.set()
                RepertoireAutomation._is_autoplay_on = False
                
                continue
        
            if not RepertoireAutomation._is_autoplay_on:
                RepertoireAutomation._game_off.clear()
                RepertoireAutomation.autoplay()

            time.sleep(0.01)
    
    def autoplay():
        for key in RepertoireAutomation._game_interface.keys:
            Threads.execute_work(RepertoireAutomation.process_key, RepertoireAutomation._game_off, key)

        RepertoireAutomation._is_autoplay_on = True

    def process_key(event: Event, key: Key) -> None:
        while not event.is_set():
            is_note_in_key = key.get_note_in_key()
            
            if is_note_in_key == "None":
                continue
            elif is_note_in_key == "Press":
                key.press()
            elif is_note_in_key == "Hold":
                key.hold()
                
            time.sleep(0.05)


if __name__ == "__main__":
    RepertoireAutomation.run()