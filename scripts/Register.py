class Register:
    def __init__(self):
        self.values = []

    def prepend(self, value: float):
        self.values.insert(0, value)

    def pop(self) -> float:
        if len(self.values) == 0:
            return None
        return self.values.pop()
