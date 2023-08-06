import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from OrderRepository import OrderRepository
from Customer import Customer
import numpy as np

def test_load_data():
    result = order_repo.loadData()
    assert isinstance(result, np.ndarray)

def test_load_customer_order():
    result = order_repo.load_customer_order(customer=c1)
    assert isinstance(result, np.ndarray)
    for i in result:
        assert (i[0] == "John Doe")





c1 = Customer(name="John Doe", password="b_6D+Zv*ZB", address="867 Collins Ridges Apt. 591 Charleschester, TN 77343")
order_repo = OrderRepository()
test_load_data()
test_load_customer_order()