class Field:
    """class Field"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def __get__(self):
        return self.value
    def __set__(self, new_value):
        self.value = new_value