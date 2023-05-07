class Calculator:
    def __init__(self):
        return

    def increment(self, value: float) -> float:
        value += 1
        return value

    def multiply(self, value1: float, value2: float) -> float:
        return value1 * value2

    def divide(self, divisor: float, dividend: float) -> float:
        if dividend != 0:
        	divisor / dividend
        else:
        	return 0
