from openKnowledgeGraph.patterns.Pattern import PropertyPattern, OrPattern, AndPattern
from openKnowledgeGraph.patterns.PatternConfig import PatternConfig
from openKnowledgeGraph.templates.Part import Part


class ArgumentPart(Part):

    def __init__(self, value):
        Part.__init__(self, value)
        self.value = value

    def get_flattened_parts(self):
        return [self]

    def get_identifier(self):
        return self.value

    def get_arguments(self):
        return [{
            "value": self.value,
            "reference": self
        }]

    def get_dof(self):
        return 1

    @property
    def preview(self):
        return "[{}]".format(self.value)

    def to_text(self):
        return "[{}]".format(self.value.full_text)

    def to_pattern(self, pattern_config: PatternConfig, current_depth_by_type={}):
        return PropertyPattern("type", self.get_value().type)

    def to_pattern2(self, properties):
        node = self.get_value()

        patterns = []
        for property in properties:
            property_value = node.__getattr__(property)

            if not property_value is None:  # does not have property
                patterns.append(PropertyPattern(property, property_value))

        return AndPattern(patterns)
