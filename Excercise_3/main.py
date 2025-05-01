from calculator import calculators
# This imports the class calculators from the calculator module

def calculator_tests():
    # This function tests the calculators class.
    calc = calculators()
    tests = [
        ("7 + 5", calc.addition, 7, 5),
        ("34 - 12", calc.subtraction, 34, 21),
        ("144 / 2", calc.division, 12, 4),
        ("45 / 0", calc.division, 45, 0),
        ("12 * 3", calc.multiplication, 12, 3),
    ]

    for desc, func, a, b in tests:
        try:
            result = func(a, b)
            print(f"{desc} = {result}")
        except Exception as e:
            print(f"{desc} = Error: {e}")



# Calling the shopping Module
from shopping import ShoppingBasket
# This imports the class ShoppingBasket from the shopping module

def shopping_tests():
    # This function tests the ShoppingBasket class.
    basket = ShoppingBasket()

# Lets add some items to the basket
    basket.add_an_item("kartofel", 4)
    basket.add_an_item("pear", 6)
    basket.add_an_item("Milch", 1)
    basket.add_an_item("brot", 3)
    
    print("Items in the basket after adding:", basket.list_items())
    # This method lists all the items in the shopping basket.
   
    print("Total items in the basket after adding:", basket.total_items())
    # This method showa the total number of items in the shopping basket.


if __name__ == "__main__":
    calculator_tests()
    # This function runs the calculator tests.
    shopping_tests()