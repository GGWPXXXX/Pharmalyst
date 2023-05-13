
from Admin import Admin
import xml.etree.ElementTree as ET

class AdminRepository:
    def __init__(self):
        self.__adminList = []
    
    def load_data(self) -> list[Admin]:
        """This method load_data reads data from an XML file containing information about Admin users, 
        and returns a list of Admin objects.

        Returns:

        List of Admin objects containing information read from the XML file.
        Raises:

        No explicit exception is raised by this method, but an error will occur if the XML file is missing or 
        incorrectly formatted."""
        tree = ET.parse('./Data/Admin/AdminToken.xml')
        root = tree.getroot()
        for a in root.findall("admin"):
            name = a.find("name").text
            password = a.find("password").text
            admin = Admin(name, password)
            self.__adminList.append(admin)
        return self.__adminList

