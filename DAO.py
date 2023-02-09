from DTO import Supplier


class _Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert_hat(self, hat):
        self._conn.execute("""
               INSERT INTO hats (id, topping, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [hat.id, hat.topping, hat.supplier, hat.quantity])


    def order_hat(self, topping):
        c = self._conn.cursor()
        toppings =c.execute("""
            SELECT id, topping, supplier, quantity FROM hats WHERE topping = (?)
        """, [topping]).fetchall()
        hat = None
        for h in toppings:
            if hat is None:
                hat = h
            elif hat[2]>h[2]:
                hat = h
        self._conn.execute("""
                    UPDATE hats SET quantity = quantity-1  WHERE topping = (?) AND supplier = (?) 
                """, [topping, hat[2]])
        self._conn.execute("""
                    DELETE FROM hats WHERE quantity = 0
                """)
        if hat is None:
            return None
        else:
            return hat







class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert_supplier(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name) VALUES (?, ?)
        """, [supplier.id, supplier.name])

    def find_supplier(self, s_id):
        c = self._conn.cursor()
        c.execute("""
                SELECT id,name FROM suppliers WHERE id = ?
            """, [s_id])

        return Supplier(*c.fetchone())


class _Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert_order(self, order):
        self._conn.execute("""
            INSERT INTO orders (id, location, hat) VALUES (?, ?, ?)
        """, [order.id, order.location, order.hat])
