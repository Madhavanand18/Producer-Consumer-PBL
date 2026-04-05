import threading
import time


class Consumer(threading.Thread):
    def __init__(self, buffer, update_callback, logger, controller):
        super().__init__()

        # Core references
        self.buffer = buffer
        self.update_callback = update_callback
        self.logger = logger
        self.controller = controller

        # Control flags
        self.running = False
        self.daemon = True   # ensures clean exit

    # ---------------- MAIN LOOP ----------------
    def run(self):
        self.running = True

        while self.running:
            try:
                # ---------------- WAITING STATE ----------------
                if self.buffer.is_empty():
                    message = "Consumer waiting (Buffer Empty)"

                    self.update_callback(
                        self.buffer.get_buffer(),
                        message
                    )

                    time.sleep(0.5 * self.controller.speed)
                    continue

                # ---------------- CONSUME ----------------
                item = self.buffer.consume()

                # Update controller stats
                self.controller.on_consume(item)

                message = f"Consumed item {item}"

                # Update UI + logs
                self.update_callback(
                    self.buffer.get_buffer(),
                    message
                )

                # Slight delay (controlled speed)
                time.sleep(1.2 * self.controller.speed)

            except Exception as e:
                # Safety: prevent thread crash
                self.update_callback(
                    self.buffer.get_buffer(),
                    f"Consumer Error: {str(e)}"
                )
                time.sleep(1)

    # ---------------- STOP ----------------
    def stop(self):
        self.running = False