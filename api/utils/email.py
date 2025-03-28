import re

class Email:

    __EMAIL_REGEX = re.compile(r"(^[\w\.-]+@[\w\.-]+\.\w+$)")

    def __init__(self, address: str):
        self.__address = self.validate(address)

    def validate(self, address: str):
        if not self.__EMAIL_REGEX.match(address):
            raise ValueError(f"Invalid E-mail: {address}")
        return address
        
    def __repr__(self):
        return self.__address
    def __str__(self):
        return self.__address
    
    @property
    def address(self):
        return self.__address