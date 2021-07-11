from openKnowledgeGraph.patterns.Pattern import MultiPartPattern
from openKnowledgeGraph.patterns.PatternConfig import PatternConfig
from openKnowledgeGraph.templates.Part import Part


class Template(Part):

    def __init__(self, value):
        Part.__init__(self, value=value)
        self.parts = []
        self.parts_by_name = {}
        self.names = []

    def matches(self, node):
        # TODO split up into parts first
        for part in self.parts:
            if not part.matches(node):
                pass

    def is_atomic(self):
        return False

    def get_arguments(self):
        arguments = []
        for part in self.parts:
            arguments += part.get_arguments()

        return arguments

    def get_nested_arguments(self):
        argument_names = []
        for name, part in self.parts_by_name.items():
            if part.get_dof() > 0:
                nested_arguments = part.get_nested_arguments()
                if len(nested_arguments) > 1:
                    for nested_argument in nested_arguments:
                        argument_names.append("{}.{}".format(name, nested_argument))
                else:
                    argument_names.append(name)

        return argument_names

    def get_text(self):
        return " ".join([p.get_text() for p in self.parts])

    def intersect(self, other):
        pass

    def get_parts_by_name(self, names):
        parts = []
        for name in names:
            if name in self.parts_by_name:
                parts.append(self.parts_by_name[name])
        return parts

    def find_argument_by_name(self, name):
        for argument in self.get_arguments():
            if argument["name"] == name:
                return argument["reference"]

        return None

    def set(self, key, value):
        argument = self.find_argument_by_name(key)
        if argument:
            argument.set_value(value)

        return self

    def get_dof(self):
        dof = 0
        for part in self.parts:
            dof += part.get_dof()

        return dof

    def add_part(self, name, part):
        index = 1
        while name in self.parts_by_name:
            name = "{}_{}".format(name, index)
            index += 1

        self.parts_by_name[name] = part
        self.names.append(name)
        self.parts.append(part)

    def flatten(self):
        flattened_parts = self.get_flattened_parts()
        template = Template(value=self.value)
        template.set_parts(flattened_parts)

        return template

    def get_flattened_parts(self):
        flattened_parts = []
        for part in self.parts:
            flattened_parts += part.get_flattened_parts()

        return flattened_parts

    def full_text(self):
        pass

    def to_text(self):
        return "{}".format(" ".join([p.to_text() for p in self.parts]))

    def __repr__(self):
        return "<Template {}>".format(self.to_text())

    def set_parts(self, parts):
        self.parts = parts

    def find_argument_nested(self):
        pass

    def get_identifier(self):
        identifiers = []
        for part in self.parts:
            identifiers.append(part.get_identifier())

        return '&'.join(identifiers)

    def __len__(self):
        return len(self.parts)

    def __iter__(self):
        for part in self.parts:
            yield part

    @staticmethod
    def get_type():
        return "default"

    def to_pattern(self, pattern_config: PatternConfig, current_depth_by_type={}):
        # config = pattern_config.get_config_for_type(self.get_type())
        # TODO if subject -> check
        sub_patterns = []
        # ignore_children=config.get_ignore_children()
        for part, name in zip(self.parts, self.names):
            # if name not in ignore_children:
            sub_patterns.append(part.to_pattern(pattern_config, current_depth_by_type))
            # else:
            #    print("ignore ", part)
        return MultiPartPattern(sub_patterns)
