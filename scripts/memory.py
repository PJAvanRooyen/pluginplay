class Memory:
    def __init__(self):
        self.value = 1

    def get(self) -> float:
        return self.value

    def set(self, value: float):
        self.value = value
