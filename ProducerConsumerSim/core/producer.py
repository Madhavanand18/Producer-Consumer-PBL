import threading
import time


class Producer(threading.Thread):
    def __init__(self, buffer, update_callback, logger, controller):
        super().__init__()

        # Core references
        self.buffer = buffer
        self.update_callback = update_callback
        self.logger = logger
        self.controller = controller

        # Control
        self.running = False
        self.daemon = True

        # Item generator
        self.counter = 1

    # ---------------- MAIN LOOP ----------------
    def run(self):
        self.running = True

        while self.running:
            try:
                # ---------------- WAITING STATE ----------------
                if self.buffer.is_full():
                    message = "Producer waiting (Buffer Full)"

                    self.update_callback(
                        self.buffer.get_buffer(),
                        message
                    )

                    time.sleep(0.5 * self.controller.speed)
                    continue

                # ---------------- PRODUCE ----------------
                item = self.counter
                self.counter += 1

                self.buffer.produce(item)

                # Update stats
                self.controller.on_produce(item)

                message = f"Produced item {item}"

                # Update UI
                self.update_callback(
                    self.buffer.get_buffer(),
                    message
                )

                # Delay based on speed
                time.sleep(1 * self.controller.speed)

            except Exception as e:
                self.update_callback(
                    self.buffer.get_buffer(),
                    f"Producer Error: {str(e)}"
                )
                time.sleep(1)

    # ---------------- STOP ----------------
    def stop(self):
        self.running = False