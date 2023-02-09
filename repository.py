import atexit
import sqlite3
import sys

from DAO import _Hats, _Suppliers, _Orders
from DTO import Hat, Supplier, Order


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect(sys.argv[4])
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)


    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
       self._conn.executescript("""
        CREATE TABLE suppliers (
            id         INTEGER      PRIMARY KEY,
            name       STRING       NOT NULL
        );
        CREATE TABLE hats (
            id           INTEGER       PRIMARY KEY,
            topping      STRING        NOT NULL,
            supplier     INTEGER       NOT NULL,
            quantity     INTEGER       NOT NULL,
            FOREIGN KEY(supplier) REFERENCES suppliers(id)
        );

        CREATE TABLE orders (
            id        INTEGER     PRIMARY KEY,
            location  STRING      NOT NULL,
            hat       INTEGER     NOT NULL,
            FOREIGN KEY(hat) REFERENCES hats(id)
        );
    """)

    def parse_text(self, file):
        with open(file) as config:
            lines = config.readlines()
        count = 0
        for line in lines:
            if count == 0:
                list = line.split(",")
                hats, suppliers = int(list[0]), int(list[1])
            elif count <= hats:
                lst = line.split(",")
                hat = Hat(int(lst[0]), lst[1], int(lst[2]), int(lst[3].strip()))
                self.hats.insert_hat(hat)
            else:
                lst = line.split(",")
                supplier = Supplier(int(lst[0]), lst[1].strip())
                self.suppliers.insert_supplier(supplier)
            count += 1

    def ex_orders(self,file):
        f = open(sys.argv[3], 'w')
        orderid = 1
        with open(file) as orders:
            lines = orders.readlines()
        for line in lines:
            line = line.strip()
            order = line.split(",")
            order_hat = self.hats.order_hat(order[1])
            supID = order_hat[2]
            if supID is not None:
                self.orders.insert_order(Order(orderid, order[0], order_hat[0]))
                f.write(order[1] + ',' + self.suppliers.find_supplier(supID).name + ',' + order[0]+'\n')
                orderid += 1



# the repository singleton

repo = _Repository()
atexit.register(repo._close)

