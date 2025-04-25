from Models.keyboard import start_keyboard

from repertoire_automation import RepertoireAutomation

from multiprocessing import Queue
from multiprocessing import Process

if __name__ == "__main__":
    keyboard_queue = Queue()

    keyboard_process = Process(target=start_keyboard, args=(keyboard_queue,))
    keyboard_process.daemon = True
    keyboard_process.start()

    RepertoireAutomation.run(keyboard_queue)