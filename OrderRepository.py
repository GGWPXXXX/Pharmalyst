import pandas as pd
from Customer import Customer

class OrderRepository:
    def __init__(self) -> None:
        self.__orderDb = pd.read_csv('./Data/Admin/Order.csv')

    def save_data(self, orderList:list()) -> None:
        """    Saves the order data in a Pandas DataFrame to a CSV file.
            Args:
            - orderList (list): A list of dictionaries containing the order data.
            Returns:
            - None: This method does not return anything."""
        new_data = pd.DataFrame(orderList)
        self.__orderDb = pd.concat([self.__orderDb, new_data], ignore_index=True)
        self.__orderDb.to_csv('./Data/Admin/Order.csv', index=False) 


    def loadData(self) -> list(): 
        
        """
        Loads the data from the "Order.csv" file and returns it as a list of values.

        Returns:
        A list of values containing the data loaded from the "Order.csv" file.

        """
        return self.__orderDb.values

    def load_customer_order(self, customer:Customer) -> list():
        """This method load_customer_order takes in a customer object of class Customer and returns a 
        list of their order data from the __orderDb attribute of the Admin class.

        Parameters:

        customer : Customer object representing the customer whose orders need to be retrieved.
        Returns:

        A list of all orders made by the given customer as numpy.ndarray object from the __orderDb 
        attribute of the Admin class. Each row of the array represents an order made by the customer."""
        return self.__orderDb.loc[self.__orderDb['Customer Name'] == customer.name].values

