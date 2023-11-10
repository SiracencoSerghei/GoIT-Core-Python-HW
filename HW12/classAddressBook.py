from collections import UserDict
import json
from classRecord import Record

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[43m"
PINK = "\033[95m"
RESET = "\033[0m"


class AddressBook(UserDict):
    """A class representing an address book that stores records."""

    def add_record(self, record):
        """Add a record to the address book.

        Args:
            record (Record): The record to add.

        Returns:
            None
        """
        if not isinstance(record, Record):
            record = Record(record)
        self.data[record.name.value] = record

    def find_name(self, name):
        """Find a record by name.

        Args:
            name (str): The name to search for.

        Returns:
            Record or None: The record if found, or None if not found.
        """
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        """Delete a record by name.

        Args:
            name (str): The name of the record to delete.

        Returns:
            None
        """
        if name in self.data:
            del self.data[name]

    def get_records(self):
        """Return a list of all records in the address book.

        Returns:
            list: A list of records."""
        return list(self.values())

    def __str__(self):
        """Return a string representation of the address book.

        Returns:
            str: A string representation of the address book.
        """
        return '\n'.join([str(r) for r in self.values()])

    def iterator(self, chunk_size=1):
        """Iterate over records in the address book in chunks.

        Args:
            chunk_size (int): The number of records to yield in each iteration.

        Yields:
            list: A list of records.
        """
        records = list(self.values())
        i = 0
        while i < len(records):
            yield records[i:i + chunk_size]
            i += chunk_size

    @staticmethod
    def convert_to_serializable(address_book):
        """Converts the AddressBook object to a serializable format.

            Args:
                address_book (AddressBook): The AddressBook object to convert.

            Returns:
                dict: A dictionary containing the serialized data.
            """
        serializable_data = {}
        for key, record in address_book.items():
            serializable_data[key] = {
                "name": record.name.value,
                "phones": record.get_all_phones(),
                "birthday": str(record.birthday) if record.birthday else None
            }
        return serializable_data

    def save_to_file(self, file_name):
        """
        Save the instance to a binary file using pickle.

        Args:
            file_name (str): The name of the file to save the instance.

        Returns:
            None
        """
        data_to_serialize = AddressBook.convert_to_serializable(self)
        print(data_to_serialize)
        with open(file_name, 'w', encoding="utf-8") as f:
            json.dump(data_to_serialize, f)

    @staticmethod
    def load_from_file(file_name):
        """
        Load an instance from a JSON file.

        Args:
            file_name (str): The name of the file to load the instance from.

        Returns:
            AddressBook: The loaded instance.
        """
        try:
            with open(file_name, 'r', encoding="utf-8") as f:
                data = json.load(f)
                address_book = AddressBook()
                for name, record_data in data.items():
                    new_record = Record(record_data['name'])
                    phones = record_data['phones']
                    birthday = record_data['birthday']
                    if birthday == 'null':
                        birthday = None
                    for phone in phones:
                        new_record.add_phone(phone)
                    if birthday is not None:
                        new_record.add_birthday(birthday)
                    address_book.add_record(new_record)
                return address_book
        except (FileNotFoundError, EOFError) as e:
            # Handle the case where the file is not found or empty
            print(e)
            return AddressBook()
    def find(self, param):
        """
        Find records that match the given parameter.

        Args:
            param (str): The search parameter.

        Returns:
            str: A string containing the matching records, separated by newline.

        Note:
            If the search parameter is less than 3 characters, it returns an error message.
        """
        if len(param) < 1:
            return "Sorry, search parameter must be more than 1 characters"
        result = []
        for record in self.values():
            # print(record)
            if param.isdigit():
                matching_phones = [phone for phone in record.get_all_phones() if param in phone]
                if matching_phones:
                    result.append(str(record))
            if record.birthday and param in str(record.birthday):
                result.append(str(record))
            elif param.isalpha() and param in record.name.value:
                result.append(str(record))
        if not result:
            return "No records found for the given parameter."
        return '\n'.join(result)
