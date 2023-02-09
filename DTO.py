class Hat:
    def __init__(self, h_id, topping, supplier, quantity):
        self.id = h_id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, s_id, name):
        self.id = s_id
        self.name = name


class Order:
    def __init__(self, o_id, location, hat):
        self.id = o_id
        self.location = location
        self.hat = hat