import sys
import os
import unittest
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from Admin import Admin
from AdminRepository import AdminRepository


class TestAdminRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.ad_repo = AdminRepository()

    def test_load_data(self):
        result = self.ad_repo.load_data()
        self.assertIsInstance(result, list)
        for i in result:
            self.assertIsInstance(i, Admin)
            
if __name__ == "__main__":
    unittest.main()
