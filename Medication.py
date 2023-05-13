class Medication:
    def __init__(self, name:str, description:str, quantity:int, category:str) -> None:
        self.__name = name
        self.__description = description
        self.__quantity = quantity
        self.__category = category

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def category(self) -> str:
        return self.__category
