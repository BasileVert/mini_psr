import tkinter as tk
from tkinter import messagebox, ttk

from recorder import PAUSED, RECORDING, Recorder
from selector import select_area


class App:
    def __init__(self, root):
        self.root = root
        self.recorder = Recorder()
        self.region = None

        self.capture_enter_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Statut : INACTIF")
        self.pause_label = tk.StringVar(value="Pause")

        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill="both", expand=True)

        ttk.Button(btn_frame, text="Selectionner une zone", command=self.select_area).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Demarrer", command=self.start).pack(fill="x", pady=4)
        ttk.Button(btn_frame, textvariable=self.pause_label, command=self.toggle_pause).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Arreter", command=self.stop).pack(fill="x", pady=4)
        ttk.Checkbutton(
            btn_frame,
            text="Capturer la touche Entree",
            variable=self.capture_enter_var,
        ).pack(fill="x", pady=4)

        ttk.Label(btn_frame, textvariable=self.status_var, anchor="w").pack(
            fill="x", pady=4
        )

    def select_area(self):
        coords = select_area(self.root)
        if coords and coords[2] > 0 and coords[3] > 0:
            self.region = coords
            self.recorder.set_region(coords)
            self.status_var.set(f"Zone selectionnee : {coords[2]}x{coords[3]}")
        else:
            messagebox.showwarning("Selection", "Aucune zone selectionnee.")

    def start(self):
        if not self.region:
            messagebox.showwarning("Demarrage", "Selectionnez une zone avant de demarrer.")
            return
        self.recorder.set_capture_enter_enabled(self.capture_enter_var.get())
        if self.recorder.start():
            self.status_var.set("Statut : ENREGISTREMENT")
            self.pause_label.set("Pause")

    def toggle_pause(self):
        if self.recorder.state == RECORDING:
            self.recorder.pause()
            self.status_var.set("Statut : EN PAUSE")
            self.pause_label.set("Reprendre")
        elif self.recorder.state == PAUSED:
            self.recorder.resume()
            self.status_var.set("Statut : ENREGISTREMENT")
            self.pause_label.set("Pause")

    def stop(self):
        self.recorder.stop(capture_on_stop=True)
        self.status_var.set("Statut : INACTIF")
        self.pause_label.set("Pause")

    def on_close(self):
        self.recorder.stop()
        self.root.destroy()
