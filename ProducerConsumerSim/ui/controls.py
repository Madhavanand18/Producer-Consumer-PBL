import tkinter as tk


class Controls:
    def __init__(self, parent):
        self.parent = parent

        self.container = tk.Frame(parent, bg="#2c2c2c")
        self.container.pack(pady=20)

        self.create_buttons()

    # ---------------- CREATE BUTTONS ----------------
    def create_buttons(self):
        self.start_btn = tk.Button(
            self.container,
            text="Start",
            width=12,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#45a049"
        )
        self.start_btn.grid(row=0, column=0, padx=15)

        self.stop_btn = tk.Button(
            self.container,
            text="Stop",
            width=12,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#d32f2f"
        )
        self.stop_btn.grid(row=0, column=1, padx=15)

        self.reset_btn = tk.Button(
            self.container,
            text="Reset",
            width=12,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#1976D2"
        )
        self.reset_btn.grid(row=0, column=2, padx=15)

    # ---------------- OPTIONAL STATE CONTROL ----------------
    def disable_all(self):
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")

    def enable_all(self):
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.reset_btn.config(state="normal")