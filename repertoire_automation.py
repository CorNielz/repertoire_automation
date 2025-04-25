from Configs import automation

from Models.game_interface import GameInterface
from Models.threads import ProcessesManager
from Models.key import Key

import time
from threading import Event

class RepertoireAutomation:
    _game_interface = GameInterface()

    _is_autoplay_on = False

    def run(keyboard_queue):
        while True:
            if not RepertoireAutomation._game_interface.is_game_on_screen():
                RepertoireAutomation._is_autoplay_on = False
                continue
        
            if not RepertoireAutomation._is_autoplay_on:
                RepertoireAutomation._is_autoplay_on = True
                RepertoireAutomation.autoplay(keyboard_queue)

            time.sleep(1)
    
    def autoplay(keyboard_queue):
        for game_key in RepertoireAutomation._game_interface.keys:
            ProcessesManager.send_work(RepertoireAutomation.process_key, game_key, keyboard_queue)

    def process_key(key: Key, keyboard_queue) -> None:
        while True:            
            have_key_been_pressed = False
            note_type = key.get_note_in_key()
            
            if note_type == "None":
                time.sleep(0.05)
                continue

            

            elif note_type == "Press":
                have_key_been_pressed = True
                keyboard_queue.put({"action": "Press", "key": key.keyboard_key})
                
            elif note_type == "Hold":
                have_key_been_pressed = True
                keyboard_queue.put({"action": "Hold", "key": key.keyboard_key})

            time.sleep(0.05)        