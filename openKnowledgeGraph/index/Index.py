from collections import defaultdict


class Index:

    def __init__(self, type):
        self.type = type
        self.key_to_values = defaultdict(list)
        self.value_to_key = {}

    def add_entry(self, key, value):
        self.key_to_values[key].append(value)
        self.value_to_key[value] = key

    def get_subselection(self, entities):
        pass

    def get_entries(self):
        entries = []
        for key, value in self.key_to_values.items():
            entries.append((key, value))
        return entries

    @staticmethod
    def get_type():
        return self.type
