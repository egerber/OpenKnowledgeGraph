from openKnowledgeGraph.queries.QueryHelper import filter_entities

DEFAULT_TEXT = "<get_text() of Entity>"


class Entity:
    """
    Base class for Nodes and Links
    """

    def __init__(self, id=None, attributes=None, **kwargs):
        if attributes is None:
            attributes = {}

        self._graph = None
        self.attributes = attributes
        self._id = id

    def set_attributes(self, attributes):
        self.attributes = attributes

    def get_attributes(self):
        return self.attributes

    def has_attribute(self, attribute):
        return attribute in self.attributes

    def get_attribute(self, name):
        return self.attributes.get(name, None)

    def has_id(self):
        return self._id is not None

    def set_id(self, new_id, override=False):
        if not override and self._id is not None and not new_id == self._id:
            raise ValueError("Trying to override id for entity (old: {}, new: {})".format(self._id, new_id))
        elif new_id is None:
            raise ValueError("Trying to assign id=None")

        self._id = new_id

    @property
    def preview(self):
        return ""

    @property
    def id(self):
        return self.get_id()

    def get_id(self):
        return self._id

    '''def __setattr__(self, key, value):
        if self.__getattr__(key) is not None:
            raise Exception(
                "Entity objects are not mutable. Properties cannot be changed after they have been defined (tried to set '{}' from '{}' to '{}')".format(
                    key, self.__getattr__(key), value))
        object.__setattr__(self, key, value)
    '''

    def __getattr__(self, name):
        if name.startswith('attr__'):
            return self.get_attribute(name[6:])
        else:
            try:
                return self.__getattribute__(name)
            except:
                return None  # default return if attribute does not exist

    @staticmethod
    def get_type():
        return "base_entity"

    def get_text(self):
        return self.text

    @property
    def lowertext(self):
        text = self.get_text()
        if isinstance(text, str):
            return text.lower()
        else:
            return text

    @property
    def type(self):
        return self.get_type()

    @property
    def graph(self):
        return self.get_graph()

    def get_graph(self):
        return self._graph

    def set_graph(self, graph):
        self._graph = graph

    def __repr__(self):
        return "<Entity ({}): {}>".format(self.get_type(), self.preview)

    def serialize(self):
        return None

    def matches(self, *queries, **query_args):
        return len(filter_entities([self], *queries, **query_args)) > 0

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    @staticmethod
    def from_db_object():
        # TODO restore from database
        pass
