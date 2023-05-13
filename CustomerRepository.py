from Customer import Customer   
import xml.etree.ElementTree as ET
import xml.dom.minidom

class CustomerRepository:
    
    def __init__(self) -> None:
        self.__customer_list = []

    def save_data(self, customerList: list[Customer]) -> None:
        """This method takes in a list of Customer objects and saves them into an XML file 
        located in the directory "./Data/Customer/CustomerToken.xml".

        The XML file has the following structure:

        <customers>
        <customer>
            <name>customer_name</name>
            <password>customer_password</password>
            <address>customer_address</address>
        </customer>
        ...
        </customers>
        Parameters:

        customerList: A list of Customer objects to be saved in the XML file.
        Returns:

        None."""
        customers = ET.Element("customers")
        for customer in customerList:
            c = ET.SubElement(customers, "customer")
            name = ET.SubElement(c, "name")
            name.text = customer.name
            password = ET.SubElement(c, "password")
            password.text = customer.password
            address = ET.SubElement(c, "address")
            address.text = customer.address
        xml_string = ET.tostring(customers, encoding='utf-8')
        dom = xml.dom.minidom.parseString(xml_string)
        with open("./Data/Customer/CustomerToken.xml", "w", encoding='utf-8') as f:
            f.write(dom.toprettyxml(indent="\t"))


    def load_data(self) -> list[Customer]:
        """Returns:
        List[Customer]: a list of Customer objects loaded from the XML file.
        """
        tree = ET.parse('./Data/Customer/CustomerToken.xml')
        root = tree.getroot()
        for c in root.findall("customer"):
            name = c.find("name").text
            password = c.find("password").text
            address = c.find("address").text
            customer = Customer(name, str(password), address)
            self.__customer_list.append(customer)

        return self.__customer_list
