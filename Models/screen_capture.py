from mss import mss
from dataclasses import dataclass
from multiprocessing import Event, Queue

import numpy
import time

class ScreenCapture():
    def __init__(self):
        self._sct = mss()
    
    def capture_screen(self, region: dict[str, int]) -> numpy.ndarray:
        sct_img = self._sct.grab(region)

        return numpy.array(sct_img)
    
class ScreenCaptureManager():
    def run(self) -> None:
        from Constants.cooldown import SCREENSHOT_INTERVAL

        screenshot_image = self._screen_capture.capture_screen(self._region)

        while not self._stop_event.is_set():
            try:
                self._screenshot_queue.put(screenshot_image, block=False)
            except:
                time.sleep(SCREENSHOT_INTERVAL)
                continue

            time.sleep(SCREENSHOT_INTERVAL)

    def __init__(self, screen_capture: ScreenCapture, screenshot_queue: Queue, region: dict[str, int]):
        self._screen_capture = screen_capture
        self._screenshot_queue = screenshot_queue
        self._stop_event = Event()
        self._region = region
        
@dataclass
class Screenshot:
    image: numpy.array = None

def start_screen_capture(region: dict[str, int], screenshot_queue: Queue):
    screen_capture = ScreenCapture()
    screen_capture_manager = ScreenCaptureManager(screen_capture, screenshot_queue, region)

    screen_capture_manager.run()

    return screen_capture_manager