from Configs import automation

from Enums.keyboard_action import KeyboardAction

from Models.game_interface import GameInterfaceDetection, GameInterface
from Models.key import Key
from Models.work import ProcessesManager

import time

class InterfaceManager:
    def __init__(self, game_interface_detection: GameInterfaceDetection):
        self._game_interface_detection = game_interface_detection

    def is_game_on_screen(self) -> bool:
        return self._game_interface_detection.is_game_on_screen()

class AutoplayManager:   
    def __init__(self, game_interface: GameInterface, key_processor: "KeyProcessor", key_group_processor: "KeyGroupProcessor", work_manager: "WorkManager", ):
        self._game_interface = game_interface
        self._key_processor = key_processor
        self._key_group_processor = key_group_processor
        self._work_manager = work_manager
        self._is_autoplay_on = False

    def start_autoplay(self, keyboard_queue):
        if self._is_autoplay_on:
            return
        
        self._is_autoplay_on = True
        self.autoplay_mode(keyboard_queue)

    def autoplay_mode(self, keyboard_queue):
        from Constants.limits import NOTES_PER_GROUP

        keys = list(self._game_interface.keys)

        for i in range(0, len(keys), NOTES_PER_GROUP):
            key_group = keys[i:i + NOTES_PER_GROUP]
            self._work_manager.send_work(self._key_group_processor.run_key_group, key_group, keyboard_queue)


    def stop_autoplay(self):
        self._work_manager.close_work(self._key_group_processor.run_key_group.__name__) 

class KeyProcessor:
    def __init__(self, note_fetcher: "NoteFetcher"):
        self._note_fetcher = note_fetcher
        self._last_found_note = None

    def run_key(self, key: Key, keyboard_queue) -> None:    
        while True:
            self.process_key(key, keyboard_queue)

            time.sleep(0.005)
            
    def process_key(self, key: Key, keyboard_queue) -> None:
        note_type = key.verify_note_type_in_key()
        
        if note_type == KeyboardAction.NONE:
            self._last_found_note = note_type
            return
        
        if note_type == self._last_found_note:
            return
        
        keyboard_queue.put({"action": note_type, "key": key.keyboard_key})
        self._last_found_note = note_type

        print(f"Note Sent to Queue: {time.time()}")

class KeyGroupProcessor:
    def __init__(self, key_processor: KeyProcessor):
        self._key_processor = key_processor

    def run_key_group(self, key_group: list[Key], keyboard_queue):
        while True:     
            for key in key_group:
                self._key_processor.process_key(key, keyboard_queue)

            time.sleep(0.005)

class NoteFetcher:
    def fetch_note_action(self, key: Key):
        return key.verify_note_type_in_key()
            
class WorkManager:
    def __init__(self, processes_manager: ProcessesManager):
        self._processes_manager = processes_manager

    def send_work(self, method, *arguments):
        self._processes_manager.send_work(method, *arguments)

    def close_work(self, method_name):
        self._processes_manager.close_process_by_name(method_name)

class RepertoireAutomation:
    def __init__(self, interface_manager: InterfaceManager, autoplay_manager: AutoplayManager):
        self._interface_manager = interface_manager
        self._autoplay_manager = autoplay_manager

    def run(self, keyboard_queue):
        from Constants.cooldown import GAME_RUNNING_CHECK

        while True:
            if not self._interface_manager.is_game_on_screen():
                self._autoplay_manager._is_autoplay_on = False
                self._autoplay_manager.stop_autoplay()
                time.sleep(GAME_RUNNING_CHECK)

                continue

            if not self._autoplay_manager._is_autoplay_on:
                self._autoplay_manager.start_autoplay(keyboard_queue)

            time.sleep(GAME_RUNNING_CHECK)