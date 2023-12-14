import sys
import os
import unittest
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from Medication import Medication
from MedicationRepository import MedicationRepository

class TestMedicationRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.meds_repo = MedicationRepository()
        self.current_dict = {"Drug_Name": "Emidoxyn 5mg Tablet 10'S",
                             "Description": "prevents lactation (production of milk) by decreasing levels of a hormone known as prolactin",
                             "Quantity": "980"}

    def test_load_data(self):
        self.assertIsInstance(self.meds_repo.load_data(category="Psychosis"), list)
        for i in self.meds_repo.load_data(category="Psychosis"):
            self.assertIsInstance(i, Medication)

    def test_load_and_compare_data(self):
        result = self.meds_repo.load_and_compare_data(
            category="Psychosis", curr_dict=self.current_dict)
        self.assertIsInstance(result, list)
        for i in result:
            self.assertIsInstance(i, Medication)
            self.assertEqual(i.category, "Psychosis")
            
if __name__ == "__main__":
    unittest.main()
