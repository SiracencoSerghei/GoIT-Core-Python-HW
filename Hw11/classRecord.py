
from className import Name
from classPhone import Phone
class Record:
    """class Record"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self,phone):
        """add phone number"""
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        self.phones.append(phone)
    def remove_phone(self, phone):
        """remove phone number"""
        if phone in [p.value for p in self.phones]:
            self.phones = [p for p in self.phones if p.value != phone]
    def edit_phone(self, old_phone, new_phone):
        """edit phone number"""
        is_found_old_phone = False
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                is_found_old_phone = True
        if not is_found_old_phone:
            raise ValueError('Phone not found')
    def find_phone(self, phone):
        """find phone by phone number"""
        for p in self.phones:
            if p.value == phone:
                return p
    def get_all_phones(self):
        """get all phones numbers"""
        result = [p.value for p in self.phones]
        return result
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
