from openKnowledgeGraph.patterns.Pattern import PropertyPattern, OrPattern
from openKnowledgeGraph.patterns.PatternConfig import PatternConfig
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart


class NPArgument(ArgumentPart):
    def __init__(self, value):
        ArgumentPart.__init__(self, value)

    def to_text(self):
        return "[{}]".format(self.value.compound_text)

    def to_pattern(self, pattern_config: PatternConfig, current_depth_by_type={}):
        return PropertyPattern("type", "np")
