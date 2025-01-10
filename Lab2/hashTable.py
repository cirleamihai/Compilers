class HashTable:
    def __init__(self):
        self.table = {}

    @staticmethod
    def hash(value):
        if isinstance(value, int):
            value = str(value)

        hash_value = 5381
        for char in value:
            hash_value = ((hash_value << 5) + hash_value) + ord(char)  # hash_value * 33 + ord(char)
        return hash_value

    def add(self, value):
        custom_hash = self.hash(value)

        if custom_hash in self.table and value not in self.table[custom_hash]:
            self.table[custom_hash].append(value)
            pos = len(self.table[custom_hash]) - 1

        else:
            self.table[custom_hash] = [value]
            pos = 0

        return custom_hash, pos

    def search(self, hash_value, pos):
        if hash_value in self.table:
            if pos < len(self.table[hash_value]):
                return self.table[hash_value][pos]

        return None

    def delete(self, hash_value, pos):
        if hash_value not in self.table or pos >= len(self.table[hash_value]):
            return

        removed_elem = self.table[hash_value].pop(pos)
        if not self.table[hash_value]:
            del self.table[hash_value]

        return removed_elem

    def __str__(self):
        return "\n" + "\n".join([f"{key}: {value}" for key, value in self.table.items()])


if __name__ == '__main__':
    table = HashTable()

    print(table.add('hello'))
    print(table.add('world'))
    print(table.add('mother'))
    print(table.add('fucker'))

    print(table.delete(210714636441, 0))

    print(table)
