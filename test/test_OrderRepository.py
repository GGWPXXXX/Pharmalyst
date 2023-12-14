import numpy as np
import sys
import os
import unittest
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from Customer import Customer
from OrderRepository import OrderRepository


class TestOrderRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.c1 = Customer(name="John Doe", password="b_6D+Zv*ZB",
                           address="867 Collins Ridges Apt. 591 Charleschester, TN 77343")
        self.order_repo = OrderRepository()

    def test_load_data(self):
        self.assertIsInstance(self.order_repo.loadData(), np.ndarray)

    def test_load_customer_order(self):
        result = self.order_repo.load_customer_order(customer=self.c1)
        self.assertIsInstance(result, np.ndarray)
        for i in result:
            self.assertEqual(i[0], "John Doe")


if __name__ == "__main__":
    unittest.main()
