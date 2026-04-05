import tkinter as tk
from ui.main_window import MainWindow


def main():
    root = tk.Tk()
    root.title("Producer-Consumer Simulator")
    root.geometry("1000x700")
    root.configure(bg="#1e1e1e")

    app = MainWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()