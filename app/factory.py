class CalculationFactory:
    @staticmethod
    def compute(calc_type, a, b):
        if calc_type == "Add":
            return a + b
        elif calc_type == "Sub":
            return a - b
        elif calc_type == "Multiply":
            return a * b
        elif calc_type == "Divide":
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        else:
            raise ValueError("Invalid calculation type")
