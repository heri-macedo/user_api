import re
import logging

logger = logging.getLogger(__name__)

class Email:
    __EMAIL_REGEX = re.compile(r"(^[\w\.-]+@[\w\.-]+\.\w+$)")

    def __init__(self, address: str):
        if not self.__EMAIL_REGEX.match(address):
            raise ValueError(f"Invalid E-mail: {address}")
        self.__address = address

    def __repr__(self):
        return f"Email({self.__address})"
    
    def __str__(self):
        return self.__address

    @property
    def address(self):
        return self.__address

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, *args, **kwargs):
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise TypeError("Email must be a string required")
        try:
            return cls(value)
        except Exception as e:
            raise ValueError("Invalid email provided") from e
