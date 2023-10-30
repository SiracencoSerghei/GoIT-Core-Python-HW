from field import Field

class Phone(Field):
    """class for validate phone number"""
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Phone number must be a ten digit string of digits")
        super().__init__(value)
    def is_valid_phone(self, value):
        """return boolean from check"""
        return value.isdigit() and len(value) == 10
