from collections import UserDict
from classRecord import Record
import pickle


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

    def save_to_file(self, file_name):
        """
        Save the instance to a binary file using pickle.

        Args:
            file_name (str): The name of the file to save the instance.

        Returns:
            None
        """
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(file_name):
        """
        Load an instance from a binary file using pickle.

        Args:
            file_name (str): The name of the file to load the instance from.

        Returns:
            object: The loaded instance.
        """
        try:
            with open(file_name, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            # Handle the case where the file is not found or empty
            return AddressBook()

    # def find(self, param):
    #     """
    #     Find records that match the given parameter.

    #     Args:
    #         param (str): The search parameter.

    #     Returns:
    #         str: A string containing the matching records, separated by newline.

    #     Note:
    #         If the search parameter is less than 3 characters, it returns an error message.
    #     """
    #     if len(param) < 3:
    #         return "Sorry, search parameter must be less than 3 characters"

    #     result = []
    #     for record in self.values():
    #         if param == str(record):
    #             result.append(str(record))

    #     return '\n'.join(result)
