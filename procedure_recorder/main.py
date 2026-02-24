import tkinter as tk
from ui import App


def main():
    root = tk.Tk()
    root.title("Mini Enregistreur de Procedure")
    root.geometry("320x220")
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
