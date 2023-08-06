class Customer:
    def __init__(self, name=None, password=None, address=None) -> None:
        if name is not None and password is not None and address is not None:
            self.__name = name
            self.__password = password
            self.__address = address
        else:
            self.__name = ''
            self.__password = ''
            self.__address = ''
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, newName) -> None:
        self.__name = newName

    @property
    def password(self) -> str:
        return self.__password
    
    @password.setter
    def password(self, newPassword) -> None:
        self.__password = newPassword

    @property
    def address(self) -> str:
        return self.__address
    
    @address.setter
    def address(self, newAddress) -> None:
        self.__address = newAddress

