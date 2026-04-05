import tkinter as tk
from tkinter import ttk

from ui.buffer_view import BufferView
from ui.controls import Controls

from core.buffer import SharedBuffer
from core.producer import Producer
from core.consumer import Consumer

from utils.logger import Logger


class MainWindow:
    def __init__(self, root):
        self.root = root

        # ---------------- CORE ----------------
        self.buffer = SharedBuffer(5)
        self.logger = Logger()

        self.produced_count = 0
        self.consumed_count = 0
        self.speed = 1.0

        # ---------------- UI ----------------
        self.setup_layout()

        self.buffer_view = BufferView(self.middle_frame)
        self.controls = Controls(self.bottom_frame)

        self.create_info_panel()
        self.create_log_panel()

        # ---------------- THREADS ----------------
        self.producer = None
        self.consumer = None

        # ---------------- BUTTONS ----------------
        self.controls.start_btn.config(command=self.start_system)
        self.controls.stop_btn.config(command=self.stop_system)
        self.controls.reset_btn.config(command=self.reset_system)

    # ---------------- LAYOUT ----------------
    def setup_layout(self):
        self.top_frame = tk.Frame(self.root, bg="#2c2c2c", height=80)
        self.top_frame.pack(fill="x")

        self.middle_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.middle_frame.pack(fill="both", expand=True)

        self.bottom_frame = tk.Frame(self.root, bg="#2c2c2c", height=100)
        self.bottom_frame.pack(fill="x")

        title = tk.Label(
            self.top_frame,
            text="Producer-Consumer Simulator",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c2c2c"
        )
        title.pack(pady=15)

    # ---------------- INFO PANEL ----------------
    def create_info_panel(self):
        frame = tk.Frame(self.middle_frame, bg="#1e1e1e")
        frame.pack(pady=10)

        self.status_label = tk.Label(frame, text="Status: Idle", fg="white", bg="#1e1e1e")
        self.status_label.pack()

        self.operation_label = tk.Label(frame, text="Operation: None", fg="cyan", bg="#1e1e1e")
        self.operation_label.pack()

        self.semaphore_label = tk.Label(frame, text="Empty: 5 | Full: 0 | Mutex: 1", fg="yellow", bg="#1e1e1e")
        self.semaphore_label.pack()

        self.stats_label = tk.Label(frame, text="Produced: 0 | Consumed: 0", fg="lightgreen", bg="#1e1e1e")
        self.stats_label.pack()

        self.speed_slider = ttk.Scale(frame, from_=0.2, to=2.0, orient="horizontal", command=self.update_speed)
        self.speed_slider.set(1.0)
        self.speed_slider.pack(pady=5)

    # ---------------- LOG PANEL ----------------
    def create_log_panel(self):
        frame = tk.Frame(self.middle_frame, bg="#1e1e1e")
        frame.pack(pady=10)

        self.log_text = tk.Text(frame, height=8, width=70, bg="#111", fg="white")
        self.log_text.pack()

    # ---------------- SPEED ----------------
    def update_speed(self, val):
        try:
            self.speed = float(val)
        except:
            self.speed = 1.0

    # ---------------- UI UPDATE ----------------
    def update_ui(self, buffer_data, message=""):
        self.buffer_view.update_buffer(buffer_data)

        if message:
            self.operation_label.config(text=f"Operation: {message}")
            self.logger.add_log(message)

            # Color highlight logic
            if "Produced" in message:
                self.buffer_view.highlight_producer()
            elif "Consumed" in message:
                self.buffer_view.highlight_consumer()
            elif "waiting" in message:
                self.buffer_view.highlight_waiting()

        self.update_logs()
        self.update_stats()
        self.update_semaphores()

    # ---------------- LOGS ----------------
    def update_logs(self):
        self.log_text.delete(1.0, tk.END)
        for log in self.logger.get_logs():
            self.log_text.insert(tk.END, log + "\n")

    # ---------------- STATS ----------------
    def update_stats(self):
        self.stats_label.config(
            text=f"Produced: {self.produced_count} | Consumed: {self.consumed_count}"
        )

    # ---------------- SEMAPHORES ----------------
    def update_semaphores(self):
        vals = self.buffer.get_semaphore_values()
        self.semaphore_label.config(
            text=f"Empty: {vals['empty']} | Full: {vals['full']} | Mutex: {vals['mutex']}"
        )

    # ---------------- START ----------------
    def start_system(self):
        if self.producer and self.producer.is_alive():
            return

        self.status_label.config(text="Status: Running", fg="green")

        self.producer = Producer(self.buffer, self.update_ui, self.logger, self)
        self.consumer = Consumer(self.buffer, self.update_ui, self.logger, self)

        self.producer.start()
        self.consumer.start()

    # ---------------- STOP ----------------
    def stop_system(self):
        self.status_label.config(text="Status: Stopped", fg="red")

        if self.producer:
            self.producer.stop()
        if self.consumer:
            self.consumer.stop()

    # ---------------- RESET ----------------
    def reset_system(self):
        self.stop_system()

        self.buffer.reset()
        self.produced_count = 0
        self.consumed_count = 0

        self.update_ui([], "System Reset")

    # ---------------- CALLBACKS ----------------
    def on_produce(self, item):
        self.produced_count += 1

    def on_consume(self, item):
        self.consumed_count += 1