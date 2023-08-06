import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Admin import Admin
from AdminManagemment import AdminManagemment



def test_find_record():
    assert(admin_manage.find_record(admin=a1) == True)
    assert(admin_manage.find_record(admin=a2) == True)
    assert(admin_manage.find_record(admin=a3) == False)

admin_manage = AdminManagemment()
a1 = Admin(name="admin13", password="dEn#SDfs")
a2 = Admin(name="admin30", password="4Y35Ck)l")
a3 = Admin(name="addmin30", password="//oink")
test_find_record()
