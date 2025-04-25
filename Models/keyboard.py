from multiprocessing import Queue

import pyautogui

from Constants.cooldown import KEY_PRESS_INTERVAL

class Keyboard:
    def run(self):
        while True:
            if self.queue.empty():
                continue
        
            request = self.queue.get()

            keyboard_key = request.get("key")
            action = request.get("action")

            if action == "Press":
                self.press(keyboard_key)
            elif action == "Hold" and not keyboard_key in self.keys_held:
                self.hold(keyboard_key)
            elif action == "Hold" and keyboard_key in self.keys_held:
                self.release(keyboard_key)

    def press(self, keyboard_key: str) -> None:        
        pyautogui.press(keyboard_key, interval=KEY_PRESS_INTERVAL)

    def hold(self, keyboard_key: str):
        pyautogui.keyDown(keyboard_key)
        self.keys_held.append(keyboard_key)

    def release(self, keyboard_key):
        pyautogui.keyUp(keyboard_key)
        self.keys_held.remove(keyboard_key)

    
    def __init__(self, queue: Queue):
        self.queue = queue
        self.keys_held = []

def start_keyboard(queue):
    keyboard = Keyboard(queue)
    keyboard.run()