import sys
import os
import unittest
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from CustomerManagement import CustomerManagement
from Customer import Customer

class TestCustomerManagement(unittest.TestCase):
    def setUp(self) -> None:
        self.custom_manage = CustomerManagement()
        self.c1 = Customer(name="John Doe", password="b_6D+Zv*ZB", address="867 Collins Ridges Apt. 591 Charleschester, TN 77343")
        self.c_fake = Customer(name="fake", password="fakepassword", address="fakeaddress")

    def test_return_record(self):
        self.assertIsInstance(self.custom_manage.return_record(self.c1.name), Customer)
        self.assertEqual(self.custom_manage.return_record(self.c1.name).name, "John Doe") 
        self.assertEqual(self.custom_manage.return_record(self.c_fake.name), None)

    def test_find_record(self):
        self.assertTrue(self.custom_manage.find_record(self.c1))
        self.assertFalse(self.custom_manage.find_record(self.c_fake))

    def test_add(self):
        self.assertFalse(self.custom_manage.add(self.c1))

    def test_create_recommendation(self):
        self.assertEqual(self.custom_manage.create_recommendation(self.c1), "Psychosis")

if __name__ == "__main__":
    unittest.main()

