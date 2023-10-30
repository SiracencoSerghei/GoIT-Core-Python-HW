from field import Field
class Name(Field):
    """class for validate name field"""
    def __init__(self, value):
        if not self.is_valid_name(value):
            raise ValueError("Name must be at least one character long")
        super().__init__(value)
    def is_valid_name(self, value):
        """return boolean from check"""
        return len(value) > 0
