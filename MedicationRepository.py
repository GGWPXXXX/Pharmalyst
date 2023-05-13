import pandas as pd
from Medication import Medication

class MedicationRepository:
    def __init__(self) -> None:
        self.__med_list = []
        self.__db = pd.read_excel('./Data/DataSet/Medicine_description.xlsx')

    def load_data(self, category:str) -> list[Medication]:
        """The load_data method loads medication data from the database for a given category and returns a 
        list of Medication objects.

        Args:

        category (str): The category of medications to load.
        Returns:

        A list of Medication objects that belong to the specified category. If there are fewer than 15 
        medications in the category, all of them will be returned. Otherwise, a random sample of 15 medications will 
        be returned."""
        self.__med_list.clear()
        category_data = self.__db[self.__db.Categories == category]
        #get at least 15 samples. If there are less than 15 samples, get all of them
        sample_size = min(15, len(category_data))
        sampled_rows = category_data.sample(n=sample_size)
        for _, row in sampled_rows.iterrows():
            medication = Medication(row['Drug_Name'], row['Description'], row['Quantity'], row['Categories'])
            self.__med_list.append(medication)
        return self.__med_list

    def load_and_compare_data(self, category:str, curr_dict:dict) -> list[Medication]:  
        """The load_and_compare_data method loads medication data from the database for a specified category, 
        compares it against a dictionary of current medications, and returns a list of up to 15 new medications
          that are not already in the dictionary.

        Args:

        category (str): A string representing the medication category to load data for.
        curr_dict (dict): A dictionary of currently selected medications to compare against.
        Returns:

        A list of up to 15 new Medication objects that are not already in curr_dict. If there are less than 15 new 
        medications available, returns all available medications."""
        self.__med_list.clear()
        category_data = self.__db[self.__db.Categories == category]
        category_data = category_data.dropna()
        count = 0
        while count < 15:
            sampled_row = category_data.sample(n=1)
            for _, row in sampled_row.iterrows():    
                medication = Medication(row['Drug_Name'], row['Description'], row['Quantity'], row['Categories'])
                if medication.name not in curr_dict:
                    self.__med_list.append(medication)
                    count += 1
        return self.__med_list
