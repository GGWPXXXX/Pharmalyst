import os
import sys
import unittest
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from AdminManagemment import AdminManagemment
from Admin import Admin


class TestAdminManagement(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Admin(name="admin13", password="dEn#SDfs")
        self.a2 = Admin(name="admin30", password="4Y35Ck)l")
        self.a3 = Admin(name="addmin30", password="//oink")
        self.admin_manage = AdminManagemment()

    def test_find_record(self):
        self.assertTrue(self.admin_manage.find_record(admin=self.a1))
        self.assertTrue(self.admin_manage.find_record(admin=self.a2))
        self.assertFalse(self.admin_manage.find_record(admin=self.a3))


if __name__ == "__main__":
    unittest.main()
