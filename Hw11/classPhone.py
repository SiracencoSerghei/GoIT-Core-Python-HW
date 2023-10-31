from field import Field


def is_valid_phone(value):
    """return boolean from check"""
    return value.isdigit() and len(value) == 10


class Phone(Field):
    """class for validate phone number"""

    def __init__(self, value):
        if not is_valid_phone(value):
            raise ValueError("Phone number must be a ten digit string of digits")
        super().__init__(value)

    def __set__(self, new_value):
        if not is_valid_phone(new_value):
            raise ValueError("Phone number must be a ten digit string of digits")
        super().__set__(new_value)
