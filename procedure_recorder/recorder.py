import threading
import time
from pathlib import Path
from typing import Optional

import mss
from PIL import Image, ImageDraw
from pynput import keyboard, mouse

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
        self.mouse_listener = None
        self.keyboard_listener = None
        self.capture_enter = False
        self.metadata = []
        self.counter = StepCounter()
        self.last_capture = 0.0
        self.lock = threading.Lock()

    def set_region(self, region):
        self.region = region
        if region:
            x, y, w, h = region
            self.monitor = {"top": y, "left": x, "width": w, "height": h}

    def set_capture_enter_enabled(self, enabled: bool):
        self.capture_enter = enabled

    def start(self):
        if not self.region:
            return False
        with self.lock:
            self.folder = create_procedure_folder()
            self.metadata = []
            self.counter.reset()
            self.last_capture = 0.0
            self.state = RECORDING
        if not self.mouse_listener or not self.mouse_listener.is_alive():
            self.mouse_listener = mouse.Listener(on_click=self._on_click)
            self.mouse_listener.daemon = True
            self.mouse_listener.start()
        if not self.keyboard_listener or not self.keyboard_listener.is_alive():
            self.keyboard_listener = keyboard.Listener(on_press=self._on_key_press)
            self.keyboard_listener.daemon = True
            self.keyboard_listener.start()
        return True

    def pause(self):
        with self.lock:
            if self.state == RECORDING:
                self.state = PAUSED

    def resume(self):
        with self.lock:
            if self.state == PAUSED:
                self.state = RECORDING

    def stop(self, capture_on_stop: bool = False):
        step = None
        with self.lock:
            can_capture = (
                capture_on_stop
                and self.state in (RECORDING, PAUSED)
                and self.monitor is not None
                and self.folder is not None
            )
            if can_capture:
                step = self.counter.next()
            self.state = IDLE

        if step is not None:
            self._capture(step, event_type="stop")

        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        self.folder = None
        self.metadata = []
        self.counter.reset()

    def _on_click(self, x, y, button, pressed):
        if not pressed:
            return
        with self.lock:
            if self.state != RECORDING or not self.monitor or not self.folder:
                return
            if not self._is_inside_region(x, y):
                return
            if not self._can_capture_now():
                return
            step = self.counter.next()
        self._capture(step, event_type="click", click_point=(x, y))

    def _on_key_press(self, key):
        if key != keyboard.Key.enter:
            return
        with self.lock:
            if self.state != RECORDING or not self.monitor or not self.folder:
                return
            if not self.capture_enter:
                return
            if not self._can_capture_now():
                return
            step = self.counter.next()
        self._capture(step, event_type="enter")

    def _can_capture_now(self) -> bool:
        now = time.time()
        if now - self.last_capture < 0.3:
            return False
        self.last_capture = now
        return True

    def _is_inside_region(self, x: int, y: int) -> bool:
        if not self.region:
            return False
        rx, ry, rw, rh = self.region
        return rx <= x < (rx + rw) and ry <= y < (ry + rh)

    def _capture(self, step: int, event_type: str, click_point=None):
        filename = f"{step}.png"
        path = self.folder / filename
        with mss.mss() as sct:
            shot = sct.grab(self.monitor)

        image = Image.frombytes("RGB", shot.size, shot.rgb)
        if event_type == "click" and click_point is not None:
            self._annotate_click(image, click_point)
        image.save(path, format="PNG", optimize=True, compress_level=9)

        entry = {"step": step, "file": filename, "event": event_type}
        with self.lock:
            self.metadata.append(entry)
            save_metadata(self.folder, self.metadata)

    def _annotate_click(self, image: Image.Image, click_point):
        click_x, click_y = click_point
        left = self.monitor["left"]
        top = self.monitor["top"]
        local_x = click_x - left
        local_y = click_y - top

        radius = 18
        draw = ImageDraw.Draw(image)
        draw.ellipse(
            (
                local_x - radius,
                local_y - radius,
                local_x + radius,
                local_y + radius,
            ),
            outline=(255, 40, 40),
            width=3,
        )
