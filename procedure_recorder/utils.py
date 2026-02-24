import json
import sys
from datetime import datetime
from pathlib import Path
import threading


class StepCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def next(self) -> int:
        with self.lock:
            self.value += 1
            return self.value

    def reset(self):
        with self.lock:
            self.value = 0


def generate_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def get_output_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd()


def create_procedure_folder(base: Path = None) -> Path:
    base = base or get_output_base_dir()
    folder = base / f"procedure_{generate_timestamp()}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def save_metadata(folder: Path, entries: list):
    path = folder / "steps.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
