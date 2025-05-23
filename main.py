from Models.game_interface import GameInterfaceDetection, ConstantsKeyDataLoader, build_game_interface
from Models.keyboard import start_keyboard
from Models.work import ProcessesManager

from repertoire_automation import RepertoireAutomation, InterfaceManager, AutoplayManager, KeyProcessor, NoteFetcher, WorkManager

from multiprocessing import Queue
from multiprocessing import Process

if __name__ == "__main__":
    keyboard_queue = Queue()

    keyboard_process = Process(target=start_keyboard, args=(keyboard_queue,))
    keyboard_process.daemon = True
    keyboard_process.start()

    game_interface_detection = GameInterfaceDetection()
    interface_manager = InterfaceManager(game_interface_detection)

    key_loader = ConstantsKeyDataLoader()
    game_interface = build_game_interface(key_loader)
    note_fetcher = NoteFetcher()
    key_processor = KeyProcessor(note_fetcher)
    processes_manager = ProcessesManager()
    work_manager = WorkManager(processes_manager)
    autoplay_manager = AutoplayManager(game_interface, key_processor, work_manager)

    repertoire_automation = RepertoireAutomation(interface_manager, autoplay_manager)

    repertoire_automation.run(keyboard_queue)