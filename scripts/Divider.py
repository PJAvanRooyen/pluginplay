class Divider:
    def divide(self, divisor: float, dividend: float) -> float:
        if divisor is not None and dividend is not None and dividend != 0:
            return divisor / dividend
        else:
            return None
