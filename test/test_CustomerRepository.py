import sys
import os
import unittest
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from CustomerRepository import CustomerRepository
from Customer import Customer

class TestCustomerRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.custom_repo = CustomerRepository()
    
    def test_load_data(self):
        self.assertIsInstance(self.custom_repo.load_data(), list)
        for i in self.custom_repo.load_data():
            self.assertIsInstance(i, Customer)

if __name__ == "__main__":
    unittest.main()
