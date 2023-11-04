class AddressBookIterator:
    def __init__(self, address_book, chunk_size=1):
        self.address_book = address_book
        self.chunk_size = chunk_size
        self.records = list(address_book.values())
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.records):
            raise StopIteration
        chunk = self.records[self.index:self.index + self.chunk_size]
        self.index += self.chunk_size
        return chunk