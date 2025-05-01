from easy_shopping import calculators, ShoppingBasket
# This imports the class ShoppingBasket from the shopping module

def demo():
    calculator = calculators()
    # This creates an instance of the calculators class.
    basket = ShoppingBasket()
    # This creates an instance of the ShoppingBasket class.

    # some small tests
    print("Addition:", calculator.addition(7, 5))
    # This method adds two numbers.
    basket.add_an_item("apple", 2)
    # This method adds an item to the shopping basket.
    print("Items in the basket are :", basket.list_items())

    # This method lists all the items in the shopping basket.

if __name__ == "__main__":
    demo()
    # This function runs the demo.