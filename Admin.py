
class Admin: 
    def __init__(self, name = None, password = None):
        if name is not None and password is not None:
            self.__name = name
            self.__password = password
        else:
            self.__name = ''
            self.__password = ''
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def password(self) -> str:
        return self.__password

    
