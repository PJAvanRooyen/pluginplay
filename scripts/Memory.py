class Memory:
    def __init__(self):
        self.value = None

    def set(self, value: float):
        self.value = value

    def get(self) -> float:
        return self.value
