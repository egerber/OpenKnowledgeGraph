import collections

from more_itertools import take

MAX_REPR_PREVIEW_ITEMS = 100


class PatternStatistics:
    '''
    TODO find common base class with GroupedEntities
    '''

    def __init__(self, pattern_to_freq):
        self.pattern_to_freq = collections.OrderedDict(
            sorted(pattern_to_freq.items(), key=lambda kv: len(kv[1]), reverse=True))

    def get_top_entities(self, k=10):
        return {k: v for k, v in take(k, self.pattern_to_freq.items())}

    def get_nth(self, n):
        return list(self.pattern_to_freq.items())[n]

    @staticmethod
    def get_type():
        return "PatternFrequencies"

    def __repr__(self):
        return_string = "<{}: \n".format(self.get_type())
        i = 0
        for pattern, templates in self.pattern_to_freq.items():
            if i < MAX_REPR_PREVIEW_ITEMS:
                return_string += "{}: {}\n".format(pattern, len(templates))
                i += 1
            else:
                break

        if len(self.pattern_to_freq) > MAX_REPR_PREVIEW_ITEMS:
            return_string += "...({} more)".format(len(self.pattern_to_freq) - MAX_REPR_PREVIEW_ITEMS)

        return return_string
