from collections import UserDict
from classRecord import Record


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

    def find(self, name):
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
