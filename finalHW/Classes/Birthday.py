from datetime import datetime
from Classes.Field import Field
RED = "\033[91m"
RESET = "\033[0m"

def is_valid_birthday(value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class Birthday(Field):
    def __init__(self, value):
        if not is_valid_birthday(value):
            print(f"{RED}The birthday date don't added to record{RESET}")
            raise ValueError("Not valid birthday date")
        super().__init__(value)

    def __set__(self, new_value):
        if not is_valid_birthday(new_value):
            raise ValueError("Not valid birthday date")
        # self.value = new_value
        super().__set__(new_value)

    def __str__(self):
        return self.value
