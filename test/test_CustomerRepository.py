import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from CustomerRepository import CustomerRepository
from Customer import Customer

def test_load_data():
    result = custom_repo.load_data()
    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, Customer)

custom_repo = CustomerRepository()
test_load_data()