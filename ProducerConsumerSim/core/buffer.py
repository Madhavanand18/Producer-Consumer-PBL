import threading


class SharedBuffer:
    def __init__(self, size=5):
        self.size = size
        self.buffer = []

        # Semaphores
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(size)
        self.full = threading.Semaphore(0)

    # ---------------- PRODUCE ----------------
    def produce(self, item):
        self.empty.acquire()
        self.mutex.acquire()

        try:
            self.buffer.append(item)
        finally:
            self.mutex.release()
            self.full.release()

    # ---------------- CONSUME ----------------
    def consume(self):
        self.full.acquire()
        self.mutex.acquire()

        try:
            item = self.buffer.pop(0)
            return item
        finally:
            self.mutex.release()
            self.empty.release()

    # ---------------- GET BUFFER ----------------
    def get_buffer(self):
        return list(self.buffer)

    # ---------------- SEMAPHORE VALUES ----------------
    def get_semaphore_values(self):
        return {
            "empty": self.empty._value,
            "full": self.full._value,
            "mutex": self.mutex._value
        }

    # ---------------- STATE CHECKS ----------------
    def is_full(self):
        return len(self.buffer) >= self.size

    def is_empty(self):
        return len(self.buffer) == 0