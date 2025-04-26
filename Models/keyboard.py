from multiprocessing import Queue
from abc import ABC, abstractmethod
import pyautogui
import time

from Constants.cooldown import KEY_PRESS_INTERVAL

from Enums.keyboard_action import KeyboardAction

class KeyboardActionHandler:
    def press(self, keyboard_key: str) -> None:        
        pyautogui.press(keyboard_key, interval=KEY_PRESS_INTERVAL)

    def hold(self, keyboard_key: str) -> None:
        pyautogui.keyDown(keyboard_key)
        self.keys_held.append(keyboard_key)
        time.sleep(KEY_PRESS_INTERVAL)

    def release(self, keyboard_key: str) -> None:
        pyautogui.keyUp(keyboard_key)
        self.keys_held.remove(keyboard_key)
        time.sleep(KEY_PRESS_INTERVAL)

    def is_held(self, keyboard_key: str) -> bool:
        return keyboard_key in self.keys_held
    
    def __init__(self):
        self.keys_held = []


class KeyboardManager:
    def run(self) -> None:
        while True:
            if self.queue.empty():
                continue
        
            request = self.queue.get()

            if not request:
                continue

            keyboard_key = request.get("key")
            action = request.get("action")

            handler = self.action_map.get(action)

            if not handler:
                continue

            handler.execute_action(keyboard_key)
       
        
    def __init__(self, queue: Queue, action_map: dict[KeyboardAction, "KeyboardActionInterface"]):
        self.queue = queue
        self.action_map = action_map


class KeyboardActionInterface(ABC):
    @abstractmethod
    def execute_action(self, keyboard_key: str) -> None:
        pass
        
class PressAction(KeyboardActionInterface):
    def __init__(self, action_handler: 'KeyboardActionHandler'):
        self.action_handler = action_handler

    def execute_action(self, keyboard_key: str) -> None:
        self.action_handler.press(keyboard_key)

class HoldAction(KeyboardActionInterface):
    def __init__(self, action_handler: 'KeyboardActionHandler'):
        self.action_handler = action_handler

    def execute_action(self, keyboard_key: str) -> None:
        if not self.action_handler.is_held(keyboard_key):
            self.action_handler.hold(keyboard_key)
        else:
            self.action_handler.release(keyboard_key)

def start_keyboard(queue: Queue) -> None:
    action_handler = KeyboardActionHandler()
    action_map: dict[KeyboardAction, KeyboardActionInterface] = {
        KeyboardAction.PRESS: PressAction(action_handler),
        KeyboardAction.HOLD: HoldAction(action_handler),
    }
    
    keyboard_manager = KeyboardManager(queue, action_map)

    keyboard_manager.run()