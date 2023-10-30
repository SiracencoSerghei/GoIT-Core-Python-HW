import time

from field import Field


class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Not valid birthday date")
        super().__init__(value)

    @staticmethod
    def is_valid_birthday(value):
        try:
            time.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def __set__(self, new_value):
        if not self.is_valid_birthday(new_value):
            raise ValueError("Not valid birthday date")
        # self.value = new_value
        super().__set__(new_value)
