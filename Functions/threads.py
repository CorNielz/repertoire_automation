from threading import Thread, Event

class Threads:
    @staticmethod
    def create_thread(method: object, event: Event, *args, is_daemon: bool = True) -> Thread:
        thread = Thread(target=method, args=(event, *args)) 
        thread.daemon = is_daemon

        return thread
    
    @staticmethod
    def run_thread(thread: Thread) -> None:
        thread.start()

    @staticmethod
    def execute_work(method: object, event: Event, *args, is_daemon: bool = True):
        work_thread = Threads.create_thread(method, event, *args)
        Threads.run_thread(work_thread)