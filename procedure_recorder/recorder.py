import threading
import time
from pathlib import Path
from typing import Optional

import mss
import mss.tools
from pynput import mouse

from utils import StepCounter, create_procedure_folder, save_metadata

IDLE = "IDLE"
RECORDING = "RECORDING"
PAUSED = "PAUSED"


class Recorder:
    def __init__(self):
        self.state = IDLE
        self.region = None
        self.monitor = None
        self.folder: Optional[Path] = None
        self.listener = None
        self.metadata = []
        self.counter = StepCounter()
        self.last_capture = 0.0
        self.lock = threading.Lock()

    def set_region(self, region):
        self.region = region
        if region:
            x, y, w, h = region
            self.monitor = {"top": y, "left": x, "width": w, "height": h}


    def start(self):
        if not self.region:
            return False
        with self.lock:
            self.folder = create_procedure_folder()
            self.metadata = []
            self.counter.reset()
            self.last_capture = 0.0
            self.state = RECORDING
        if not self.listener or not self.listener.is_alive():
            self.listener = mouse.Listener(on_click=self._on_click)
            self.listener.daemon = True
            self.listener.start()
        return True

    def pause(self):
        with self.lock:
            if self.state == RECORDING:
                self.state = PAUSED

    def resume(self):
        with self.lock:
            if self.state == PAUSED:
                self.state = RECORDING

    def stop(self):
        with self.lock:
            self.state = IDLE
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.folder = None
        self.metadata = []
        self.counter.reset()

    def _on_click(self, x, y, button, pressed):
        if not pressed:
            return
        with self.lock:
            if self.state != RECORDING or not self.monitor or not self.folder:
                return
            now = time.time()
            if now - self.last_capture < 0.3:
                return
            self.last_capture = now
            step = self.counter.next()
        self._capture(step)

    def _capture(self, step: int):
        filename = f"{step}.png"
        path = self.folder / filename
        with mss.mss() as sct:
            shot = sct.grab(self.monitor)
            mss.tools.to_png(shot.rgb, shot.size, output=str(path))
        entry = {"step": step, "file": filename}
        with self.lock:
            self.metadata.append(entry)
            save_metadata(self.folder, self.metadata)

