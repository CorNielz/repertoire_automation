from multiprocessing import Queue

import pyautogui

from Constants.cooldown import KEY_PRESS_INTERVAL

from Enums.keyboard_action import KeyboardAction

class KeyboardActionHandler:
    def press(self, keyboard_key: str) -> None:        
        pyautogui.press(keyboard_key, interval=KEY_PRESS_INTERVAL)

    def hold(self, keyboard_key: str) -> None:
        pyautogui.keyDown(keyboard_key)
        self.keys_held.append(keyboard_key)

    def release(self, keyboard_key: str) -> None:
        pyautogui.keyUp(keyboard_key)
        self.keys_held.remove(keyboard_key)

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

            handler(keyboard_key)

    def _handle_press(self, keyboard_key: str) -> None:
        self.action_handler.press(keyboard_key)

    def _handle_hold(self, keyboard_key: str) -> None:
        if not self.action_handler.is_held(keyboard_key):
            self.action_handler.hold(keyboard_key)
        else:
            self.action_handler.release(keyboard_key)
        
    def __init__(self, queue: Queue, action_handler: KeyboardActionHandler):
        self.queue = queue
        self.action_handler = action_handler

        self.action_map = {
            KeyboardAction.PRESS: self._handle_press,
            KeyboardAction.HOLD: self._handle_hold,
        }
        


def start_keyboard(queue: Queue) -> None:
    action_handler = KeyboardActionHandler()
    keyboard_manager = KeyboardManager(queue, action_handler)

    keyboard_manager.run()