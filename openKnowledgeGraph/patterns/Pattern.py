from __future__ import annotations

from openKnowledgeGraph.templates.Part import Part


class Pattern:

    def __init__(self, **kwargs):
        pass

    def get_type(self) -> str:
        return "BASE"

    def __hash__(self):
        raise NotImplementedError()

    def __call__(self, node):
        return self.matches(node)

    def matches(self, template: Part) -> bool:
        raise NotImplementedError()

    def __and__(self, other):
        if self == other:
            return self
        else:
            return FalsePattern()

    def __or__(self, other_pattern) -> Pattern:
        if self == other_pattern:
            return self
        else:
            return OrPattern(patterns=[self, other_pattern])

    def get_preview_string(self) -> str:
        return ""

    def __repr__(self) -> str:
        return "<{}: {}>".format(self.get_type(), self.get_preview_string())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)


class FalsePattern(Pattern):

    def __init__(self):
        Pattern.__init__(self)

    def get_type(self) -> str:
        return "FALSE"

    def __hash__(self):
        return hash(False)

    def matches(self, node):
        return False

    def __repr__(self):
        return "<False>"


class AndPattern(Pattern):

    def __init__(self, patterns):
        Pattern.__init__(self)
        self.patterns = get_unique_patterns(patterns)

    def matches(self, node):
        for pattern in self.patterns:
            if not pattern.matches(node):
                return False

        return True

    def get_patterns(self):
        return self.patterns

    @staticmethod
    def get_type():
        return "AND"

    def __and__(self, other):
        if self == other:
            return self
        if other.get_type() == "AND":
            return AndPattern(patterns=self.get_patterns() + other.get_patterns())
        else:
            return AndPattern(patterns=[self, other])

    def __or__(self, other):
        if self == other:
            return self

        return OrPattern(patterns=[self, other])

    def __hash__(self):
        sub_patterns = list(sorted([hash(pattern) for pattern in self.patterns]))
        return hash(("AND", hash(tuple(sub_patterns))))

    def get_preview_string(self):
        return "({})".format(' AND '.join([pattern.__repr__() for pattern in self.get_patterns()]))


class TextPattern(Pattern):
    def __init__(self, text):
        Pattern.__init__(self)
        self.text = text

    @staticmethod
    def get_type():
        return "TEXT"

    def get_preview_string(self) -> str:
        return self.text

    def __hash__(self):
        return hash(("TEXT", self.text))

    def matches(self, template: Part):
        return template.get_property("text") == self.text


class PropertyPattern(Pattern):

    def __init__(self, property_name, property_value):
        Pattern.__init__(self)
        self.property_name = property_name
        self.property_value = property_value

    def __hash__(self):
        return hash(("PROPERTY", self.property_name, self.property_value))

    @staticmethod
    def get_type():
        return "PROPERTY"

    def matches(self, template: Part):
        return template.get_property(self.property_name) == self.property_value

    def get_preview_string(self):
        return "{}={}".format(self.property_name, self.property_value)


def get_unique_patterns(patterns):
    unique_patterns = []
    for pattern in patterns:
        if pattern in unique_patterns:
            continue
        unique_patterns.append(pattern)

    return unique_patterns


def get_intersection(patterns1, patterns2):
    intersection_patterns = []
    for pattern in patterns1:
        if pattern in patterns2:
            intersection_patterns.append(pattern)

    return intersection_patterns


class OrPattern(Pattern):

    def __init__(self, patterns):
        Pattern.__init__(self)
        self.patterns = get_unique_patterns(patterns)

    def matches(self, template):
        for pattern in self.patterns:
            if pattern.matches(template):
                return True

        return False

    @staticmethod
    def get_type():
        return "OR"

    def get_patterns(self) -> [Pattern]:
        return self.patterns

    def __or__(self, other: Pattern):
        if other.get_type() == "OR":
            return OrPattern(patterns=self.get_patterns() + other.get_patterns())
        else:
            return OrPattern(patterns=[self, other])

    def __and__(self, other: Pattern):
        if self == other:
            return self

        return AndPattern(patterns=[self, other])

    def intersect(self, other_pattern):
        if other_pattern.get_type() == "OR":
            intersect_patterns = get_intersection(self.get_patterns(), other_pattern.get_patterns())
            return OrPattern(patterns=intersect_patterns)
        else:
            raise NotImplementedError()

    def union(self, other_pattern):
        # TODO merge patterns that have the same type (e.g. ner=person and ner=company => ner=[person,company])

        raise NotImplementedError()

    def __hash__(self):
        sub_patterns = list(sorted([hash(pattern) for pattern in self.patterns]))
        return hash(("OR", hash(tuple(sub_patterns))))

    def get_preview_string(self):
        return "({})".format(' OR '.join([pattern.__repr__() for pattern in self.get_patterns()]))


class MultiPartPattern(Pattern):
    '''
    Pattern that includes various sub patterns
    '''

    def __init__(self, patterns):
        Pattern.__init__(self)
        self.patterns = patterns
        self.len = len(self.patterns)

    def matches(self, template: Part) -> bool:
        if not template.is_atomic():
            if not len(template) == len(self):
                return False
            for self_part, other_part in zip(self, template):
                if not self_part.matches(other_part):
                    return False
            return True
        elif len(self) == 1:
            return self.patterns[0].matches(template)
        else:
            return False

    def __hash__(self):
        sub_patterns = list(sorted([hash(pattern) for pattern in self.patterns]))
        return hash(("MULTIPART", hash(tuple(sub_patterns))))

    def __iter__(self):
        for pattern in self.patterns:
            yield pattern

    def get_preview_string(self):
        return "[{}]".format('+'.join([pattern.get_preview_string() for pattern in self]))

    def __len__(self):
        return self.len

    @staticmethod
    def get_type():
        return "MULTIPART"


class PatternFactory:

    @staticmethod
    def from_node(node, properties=None):
        if properties is None:
            properties = ["text", "lemma", "dep", "pos", "ner"]

        patterns = []
        for property_name in properties:
            patterns.append(
                PropertyPattern(property_name=property_name, property_value=node.__getattr__(property_name)))

        return OrPattern(patterns=patterns)
