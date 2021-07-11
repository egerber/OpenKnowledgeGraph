from openKnowledgeGraph.patterns.Pattern import PropertyPattern, TextPattern
from openKnowledgeGraph.patterns.PatternConfig import PatternConfig
from openKnowledgeGraph.templates.Part import Part


class TextPart(Part):
    def __init__(self, value):
        Part.__init__(self, value)
        self.value = value

    def get_identifier(self):
        return self.value

    def get_property(self, name):
        if name == "text":
            return self.get_value()
        else:
            return None

    def get_flattened_parts(self):
        return [self]

    def fill(self):
        # nothing to fill
        pass

    def to_pattern(self,pattern_config:PatternConfig,current_depth_by_type={}):
        return TextPattern(self.get_value())
