import tkinter as tk


class BufferView:
    def __init__(self, parent, size=5):
        self.parent = parent
        self.size = size
        self.cells = []

        # Container
        self.container = tk.Frame(parent, bg="#1e1e1e")
        self.container.pack(pady=25)

        self.create_buffer()

    # ---------------- CREATE BUFFER ----------------
    def create_buffer(self):
        for i in range(self.size):
            frame = tk.Frame(self.container, bg="#1e1e1e")
            frame.grid(row=0, column=i, padx=10)

            # Slot label
            slot_label = tk.Label(
                frame,
                text=f"Slot {i}",
                fg="lightgray",
                bg="#1e1e1e",
                font=("Arial", 9)
            )
            slot_label.pack(pady=3)

            # Actual buffer cell
            cell = tk.Label(
                frame,
                text="",
                width=8,
                height=4,
                bg="#2c2c2c",
                fg="white",
                borderwidth=2,
                relief="solid",
                font=("Arial", 10, "bold")
            )
            cell.pack()

            self.cells.append(cell)

    # ---------------- UPDATE BUFFER ----------------
    def update_buffer(self, buffer_data):
        for i in range(self.size):
            if i < len(buffer_data):
                # Filled cell → green
                self.cells[i].config(
                    text=str(buffer_data[i]),
                    bg="#4CAF50"
                )
            else:
                # Empty cell → dark
                self.cells[i].config(
                    text="",
                    bg="#2c2c2c"
                )

    # ---------------- HIGHLIGHT ACTION ----------------
    def highlight_producer(self):
        for cell in self.cells:
            cell.config(bg="#4CAF50")

    def highlight_consumer(self):
        for cell in self.cells:
            cell.config(bg="#f44336")

    def highlight_waiting(self):
        for cell in self.cells:
            cell.config(bg="#FFC107")