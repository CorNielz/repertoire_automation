from multiprocessing import Process

class ProcessesManager:
    def __init__(self):
        self._processes: list[Process] = []

    def send_work(self, method, *arguments):
        process = Process(target=method, args=arguments)
        process.name = method.__name__
        process.start()

        self._processes.append(process)

    def close_process_by_name(self, method_name: str):
        for process in self._processes:
            if process.is_alive() and process.name == method_name:
                process.terminate()
                self._processes.remove(process)

    def stop_all_processes(self):
        for process in self._processes:
            if process.is_alive():
                process.terminate()

        self._processes.clear()