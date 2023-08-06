import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MedicationRepository import MedicationRepository
from Medication import Medication

def test_load_data():
    result = meds_repo.load_data(category="Psychosis")
    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, Medication)

def test_load_and_compare_data():
    result = meds_repo.load_and_compare_data(category="Psychosis", curr_dict=current_dict)
    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, Medication)
        assert(i.category == "Psychosis")
    

meds_repo = MedicationRepository()
test_load_data()
current_dict = {"Drug_Name": "Emidoxyn 5mg Tablet 10'S", 
             "Description": "prevents lactation (production of milk) by decreasing levels of a hormone known as prolactin",
             "Quantity": "980"}
test_load_and_compare_data()
