class Logger:
    def __init__(self):
        self.logs = []

    def add_log(self, message):
        self.logs.append(message)

        # keep only last 10 logs
        if len(self.logs) > 10:
            self.logs.pop(0)

    def get_logs(self):
        return self.logs