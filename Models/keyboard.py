from multiprocessing import Queue
from abc import ABC, abstractmethod
import pyautogui
import time
import asyncio

from Enums.keyboard_action import KeyboardAction

class KeyboardActionHandler:
    def press(self, keyboard_key: str) -> None:        
        pyautogui.press(keyboard_key)

        print(f"Note Executed: {time.time()}")

    def hold(self, keyboard_key: str) -> None:
        pyautogui.keyDown(keyboard_key)
        self.keys_held.append(keyboard_key)

        print(f"Note Executed: {time.time()}")

    def release(self, keyboard_key: str) -> None:
        pyautogui.keyUp(keyboard_key)
        self.keys_held.remove(keyboard_key)

    def is_held(self, keyboard_key: str) -> bool:
        return keyboard_key in self.keys_held
    
    def __init__(self):
        self.keys_held = []


class KeyboardManager:
    async def run(self) -> None:
        while True:
            if self.queue.empty():
                await asyncio.sleep(0.001)

            request = self.queue.get()

            if request:
                keyboard_key = request.get("key")
                action = request.get("action")

                handler = self.action_map.get(action)

                if handler:
                    print(f"Note Received in Queue: {time.time()}")
                    await handler.execute_action(keyboard_key)

        
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

    async def execute_action(self, keyboard_key: str) -> None:
        self.action_handler.press(keyboard_key)

class HoldAction(KeyboardActionInterface):
    def __init__(self, action_handler: 'KeyboardActionHandler'):
        self.action_handler = action_handler

    async def execute_action(self, keyboard_key: str) -> None:
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

    asyncio.run(keyboard_manager.run())