from AdminRepository import AdminRepository
from Admin import Admin

class AdminManagemment(Admin):
    def __init__(self) -> None:
        self.__admin_repo = AdminRepository()
        self.__admin_list = []
    
    def insert_adminList(self) -> None:
        """This method updates the local admin list by loading data from the admin 
        repository and merging it with the existing admin list. It then updates the admin 
        list to include any new admin data.

        Args:

        None
        Returns:

        None"""
        admin_set = set(self.__admin_list)
        admin_set.update(self.__admin_repo.load_data())
        self.__admin_list = list(admin_set)
    
    def find_record(self, admin:Admin) ->bool:
        """This method takes an admin object and checks if the admin's name and password match any record in the 
        self.__adminList. If there is a match, it returns True, otherwise, it returns False.

        Args:

        admin: An Admin object that contains the name and password of the admin to search for in the list of admins.
        Returns:

        A boolean value. True if the admin's name and password match any record in the list of admins, otherwise False."""
        self.insert_adminList()
        for Xadmin in self.__admin_list:
            if Xadmin.name == admin.name and Xadmin.password == admin.password: return True          
        return False
