from multiprocessing import Queue

import pyautogui

from Constants.cooldown import KEY_PRESS_INTERVAL

from Enums.keyboard_action import KeyboardAction

class KeyboardActionHandler:
    def press(self, keyboard_key: str) -> None:        
        pyautogui.press(keyboard_key, interval=KEY_PRESS_INTERVAL)

    def hold(self, keyboard_key: str):
        pyautogui.keyDown(keyboard_key)
        self.keys_held.append(keyboard_key)

    def release(self, keyboard_key):
        pyautogui.keyUp(keyboard_key)
        self.keys_held.remove(keyboard_key)

    def __init__(self):
        self.keys_held = []


class KeyboardManager:
    def run(self):
        while True:
            if self.queue.empty():
                continue
        
            request = self.queue.get()

            keyboard_key = request.get("key")
            action = request.get("action")

            if action == KeyboardAction.PRESS:
                self.press(keyboard_key)
            elif action == KeyboardAction.HOLD and not keyboard_key in self.keys_held:
                self.hold(keyboard_key)
            elif action == KeyboardAction.HOLD and keyboard_key in self.keys_held:
                self.release(keyboard_key)

    def __init__(self, queue: Queue, action_handler: KeyboardActionHandler):
        self.queue = queue
        self.action_handler = action_handler

    

def start_keyboard(queue: Queue):
    action_handler = KeyboardActionHandler()
    keyboard_manager = KeyboardManager(queue, action_handler)

    keyboard_manager.run()