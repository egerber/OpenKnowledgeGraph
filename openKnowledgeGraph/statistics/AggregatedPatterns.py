from __future__ import annotations


class AggregatedPatterns:

    def __init__(self, pattern_counter, instances_by_pattern):
        self.pattern_counter = pattern_counter
        self.instances_by_pattern = instances_by_pattern

    def preview(self, n: int = 25):
        return_string = ""
        i = 0
        for pattern, counter in self.pattern_counter.most_common(n):
            return_string += "[{}] {}: {}\n".format(i, pattern, counter)
            i += 1

        if len(self.pattern_counter) > n:
            return_string += "...({} more)".format(len(self.pattern_counter) - n)

        return return_string

    def nth(self, n: int):
        return self.pattern_counter.most_common(n + 1)[n][0]

    def nth_examples(self, n: int):
        return self.instances_by_pattern[self.nth(n)]

    def __getitem__(self, pattern):
        return self.instances_by_pattern[pattern]

    def __add__(self, aggregated_patterns: AggregatedPatterns):
        '''
        joins the distributions of two aggregated patterns
        returns new collection
        :return: 
        '''
        pass

    def __repr__(self):
        return f"<AggregatedPatterns: {self.preview()}>"
