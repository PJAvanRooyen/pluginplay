class Register:
    def __init__(self):
        self.values = []

    def prepend(self, value: float):
        self.values.prepend(value)

    def pop(self) -> float:
        return self.values.pop()
