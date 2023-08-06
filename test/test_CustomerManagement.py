import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from CustomerManagement import CustomerManagement
from Customer import Customer

def test_return_record():
    assert isinstance(custom_manage.return_record(c1.name), Customer)
    assert(custom_manage.return_record(c1.name).name=="John Doe") 
    assert(custom_manage.return_record(c_fake.name)==None)

def test_find_record():
    assert(custom_manage.find_record(c1) == True)
    assert(custom_manage.find_record(c_fake) == False)

def test_add():
    assert(custom_manage.add(c1) == False)

def test_create_recommendation():
    assert(custom_manage.create_recommendation(c1) == "Psychosis")



custom_manage = CustomerManagement()

c_fake = Customer(name="fake", password="fakepassword", address="fakeaddress")

test_return_record()
test_find_record()
test_add()
test_create_recommendation()

c1 = Customer(name="John Doe", password="b_6D+Zv*ZB", address="867 Collins Ridges Apt. 591 Charleschester, TN 77343")