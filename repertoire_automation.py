from Configs import automation

from Constants.cooldown import IS_GAME_RUNNING, NOTE_DETECTION

from Enums.keyboard_action import KeyboardAction

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

            time.sleep(IS_GAME_RUNNING)
    
    def autoplay(keyboard_queue):
        for game_key in RepertoireAutomation._game_interface.keys:
            ProcessesManager.send_work(RepertoireAutomation.process_key, game_key, keyboard_queue)

    def process_key(key: Key, keyboard_queue) -> None:
        while True:            
            have_key_been_pressed = False
            note_type = key.get_note_in_key()
            
            if note_type == KeyboardAction.NONE:
                time.sleep(NOTE_DETECTION)
                continue

            

            elif note_type == KeyboardAction.PRESS:
                have_key_been_pressed = True
                keyboard_queue.put({"action": KeyboardAction.PRESS, "key": key.keyboard_key})
                
            elif note_type == KeyboardAction.HOLD:
                have_key_been_pressed = True
                keyboard_queue.put({"action": KeyboardAction.HOLD, "key": key.keyboard_key})

            time.sleep(NOTE_DETECTION)        