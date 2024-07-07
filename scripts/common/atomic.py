import threading


class AtomicInt:
    def __init__(self, initial=0):
        self.value = initial
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def wait_until_gte(self, threshold: int = 1):
        with self.lock:
            while self.value < threshold:
                self.condition.wait()
            return self.value

    def increment(self, value: int = 1):
        with self.lock:
            self.value += value
            self.condition.notify_all()
            return self.value

    def decrement(self, value: int = 1):
        with self.lock:
            self.value -= value
            self.condition.notify_all()
            return self.value

    def get(self):
        with self.lock:
            return self.value

    def set(self, new_value: int):
        with self.lock:
            self.value = new_value
            self.condition.notify_all()
