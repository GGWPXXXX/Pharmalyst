import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from AdminRepository import AdminRepository
from Admin import Admin
def test_load_data():
    result = ad_repo.load_data()
    assert isinstance(result, list)
    for i in result :
        assert isinstance(i, Admin)

ad_repo = AdminRepository()
test_load_data()