from Configs import automation

from Enums.keyboard_action import KeyboardAction

from Models.game_interface import GameInterfaceDetection, GameInterface
from Models.work import ProcessesManager
from Models.key import Key

import time

class InterfaceManager:
    def __init__(self, game_interface_detection: GameInterfaceDetection):
        self._game_interface_detection = game_interface_detection

    def is_game_on_screen(self) -> bool:
        return self._game_interface_detection.is_game_on_screen()

class AutoplayManager:   
    def __init__(self, game_interface: GameInterface, key_processor: "KeyProcessor", work_manager: "WorkManager"):
        self._game_interface = game_interface
        self._work_manager = work_manager
        self._key_processor = key_processor
        self._is_autoplay_on = False

    def start_autoplay(self, keyboard_queue):
        self._is_autoplay_on = True
        self.autoplay_mode(keyboard_queue)

    def autoplay_mode(self, keyboard_queue):
        for game_key in self._game_interface.keys:
            self._work_manager.send_work(self._key_processor.process_key, (game_key, keyboard_queue))

class KeyProcessor:
    def __init__(self, note_fetcher: "NoteFetcher"):
        self._note_fetcher = note_fetcher

    def process_key(self, key: Key, keyboard_queue) -> None:
        from Constants.cooldown import NOTE_DETECTION

        while True:            
            have_key_been_pressed = False
            note_type = key.verify_note_type_in_key()
            
            if note_type == KeyboardAction.NONE:
                time.sleep(NOTE_DETECTION)
                continue

            keyboard_queue.put({"action": KeyboardAction.PRESS, "key": key.keyboard_key})
            time.sleep(NOTE_DETECTION)    

class NoteFetcher:
    def fetch_note_action(self, key: Key):
        return key.verify_note_type_in_key()
            
class WorkManager:
    def __init__(self, processes_manager: ProcessesManager):
        self._processes_manager = processes_manager

    def send_work(self, method, *arguments):
        self._processes_manager.send_work(method, *arguments)

class RepertoireAutomation:
    def __init__(self, interface_manager: InterfaceManager, autoplay_manager: AutoplayManager, ):
        self._interface_manager = interface_manager
        self._autoplay_manager = autoplay_manager

    def run(self, keyboard_queue):
        from Constants.cooldown import GAME_RUNNING_CHECK

        while True:
            if not self._interface_manager.is_game_on_screen():
                self._autoplay_manager._is_autoplay_on = False
                continue

            if not self._autoplay_manager._is_autoplay_on:
                self._autoplay_manager.start_autoplay(keyboard_queue)

            time.sleep(GAME_RUNNING_CHECK)