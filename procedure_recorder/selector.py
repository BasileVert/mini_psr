import tkinter as tk

import mss


def select_area(parent):
    selection = {"start": None, "rect": None, "coords": None, "canvas": None}
    with mss.mss() as sct:
        monitors = sct.monitors[1:]
    if not monitors:
        return None

    overlays = []
    done = tk.BooleanVar(parent, False)

    def close_all():
        for overlay in overlays:
            if overlay.winfo_exists():
                overlay.destroy()

    def on_press(event):
        current_canvas = event.widget
        if selection["rect"] and selection["canvas"] and selection["canvas"].winfo_exists():
            selection["canvas"].delete(selection["rect"])
        selection["canvas"] = current_canvas
        selection["start"] = (event.x_root, event.y_root)
        selection["rect"] = current_canvas.create_rectangle(
            event.x,
            event.y,
            event.x,
            event.y,
            outline="red",
            width=2,
        )

    def on_drag(event):
        if not selection["start"] or not selection["canvas"] or not selection["rect"]:
            return
        canvas = selection["canvas"]
        if not canvas.winfo_exists():
            return
        x0_root, y0_root = selection["start"]
        canvas_x = canvas.winfo_rootx()
        canvas_y = canvas.winfo_rooty()
        x1_root, y1_root = event.x_root, event.y_root
        canvas.coords(
            selection["rect"],
            x0_root - canvas_x,
            y0_root - canvas_y,
            x1_root - canvas_x,
            y1_root - canvas_y,
        )

    def on_release(event):
        if not selection["start"]:
            return
        x0, y0 = selection["start"]
        x1, y1 = event.x_root, event.y_root
        x, y = min(x0, x1), min(y0, y1)
        w, h = abs(x1 - x0), abs(y1 - y0)
        selection["coords"] = (x, y, w, h)
        done.set(True)
        close_all()

    def on_cancel(_event=None):
        selection["coords"] = None
        done.set(True)
        close_all()

    for mon in monitors:
        overlay = tk.Toplevel(parent)
        overlay.attributes("-alpha", 0.2)
        overlay.attributes("-topmost", True)
        overlay.overrideredirect(True)
        overlay.config(cursor="crosshair")
        overlay.geometry(
            f'{mon["width"]}x{mon["height"]}{mon["left"]:+d}{mon["top"]:+d}'
        )
        canvas = tk.Canvas(overlay, bg="black", highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        overlay.bind("<Escape>", on_cancel)
        overlays.append(overlay)

    if overlays:
        overlays[0].focus_force()
    parent.wait_variable(done)
    return selection["coords"]
