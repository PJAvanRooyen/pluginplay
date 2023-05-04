class Incrementer:
    def __init__(self):
        self.value = None

    def increment(self, value: int) -> int:
        value += 1
        self.value = value
        return self.value

    def increment2(self, value: int) -> int:
        value += 1
        self.value = value
        return self.value

    def increment3(self, value: int) -> int:
        value += 1
        self.value = value
        return self.value