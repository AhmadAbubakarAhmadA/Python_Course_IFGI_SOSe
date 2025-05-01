class calculators:
    # This class is a calculator that does addition, subtraction, multiplication, and division.

    def addition(self, a, b):
        # this method add two numbers
        return a + b
    
    def subtraction(self, a, b_):
        # this method subtracts two numbers
        return a - b_
    
    def division(self, a ,b):
        # this method divides two numbers
        if b == 0:
            raise ValueError("This cannot be allowed")
        return a / b
    
    def multiplication(self, a, b):
        # this method multiplies two numbers
        return a * b
    