from openKnowledgeGraph.patterns.PatternConfig import PatternConfig
from openKnowledgeGraph.patterns.Patterns import Patterns


class Templates:

    def __init__(self, templates):
        self.templates = templates

    def to_patterns(self, pattern_config: PatternConfig) -> Patterns:
        return Patterns([template.to_pattern(pattern_config) for template in self])

    def group(self):
        pass

    def __getitem__(self, item):
        return self.templates[item]

    def __iter__(self):
        for template in self.templates:
            yield template
