from openKnowledgeGraph.patterns.PatternConfig import PatternConfig
from openKnowledgeGraph.patterns.PatternStatistics import PatternStatistics


class Patterns:

    def __init__(self, patterns=None):
        if patterns is None:
            self.patterns = []
        else:
            self.patterns = unique_itemspatterns))

    def group(self):
        pass

    def __getitem__(self, item):
        return self.patterns[item]

    def get_statistics(self, templates, pattern_config: PatternConfig):
        '''
        return {Pattern -> freq} dict
        :param templates:
        :return:
        '''

        stats = {pattern: [] for pattern in self}
        for template in templates:
            stats[template.to_pattern(pattern_config)].append(template)

        return PatternStatistics(stats)

    def append(self, pattern):
        if pattern not in self.patterns:
            self.patterns.append(pattern)

    def __iter__(self):
        for pattern in self.patterns:
            yield pattern
