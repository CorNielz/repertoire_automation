from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor

class ProcessesManager:
    def send_work(self, method, *arguments):
        process = Process(target=method, args=arguments)
        process.start()

    