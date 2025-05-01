class ShoppingBasket:
    # This class represents a shopping basket.

    def __init__(self):
        # This method initiates the shopping basket.
        self.items = {}
        # This initializes the items in the shopping basket.

    def add_an_item(self, name, Quantity=1):
        # This method adds an item to the shopping basket.
        if Quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self.items[name] = self.items.get(name, 0) + Quantity
        # This adds the quantity of the item to the shopping basket.

    def remove_an_item(self, name, Quantity=1):
        # This method removes an item from the shopping basket.
        if name not in self.items:
            raise ValueError("Item is not in the basket")
        if Quantity is None or Quantity >= self.items[name]:
            del self.items[name]
        else:
            self.items[name] -= Quantity
        # This method removes the quantity of an item from the shopping basket.

    def total_items(self):
        # This method returns the total number of items in the shopping basket.
        return sum(self.items.values())
        # This calculates the total number of items in the shopping basket.

    def list_items(self):
        # This method lists all the items in the shopping basket.
        return dict(self.items)
        # This returns a dictionary of all items in the shopping basket.