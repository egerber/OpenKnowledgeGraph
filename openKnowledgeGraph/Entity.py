from openKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.queries.QueryHelper import filter_entities

DEFAULT_TEXT = "<get_text() of Entity>"


class Entity:
    """
    Base class for Nodes and Links
    """

    def __init__(self, graph=None,id=None, attributes=None,**kwargs):
        if attributes is None:
            attributes = {}

        if graph is None:
            raise ValueError("reference to graph required, 'None' given")

        self._graph = graph
        self.attributes = attributes
        self._id = id

        if kwargs is not None:
            for key, value in kwargs.items():
                self.set_property(key,value)

        #id and type are saved by default
        self.set_property("id",id)
        
        #self.set_property("type",kwargs['type'])


    def set_property(self,key,value):
        raise NotImplementedError()

    def get_property(self,key):
        raise NotImplementedError()

    def has_property(self,key):
        raise NotImplementedError()

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
        if not override and self._id is not None and new_id != self._id:
            raise ValueError("Trying to override id for entity (old: {}, new: {})".format(self._id, new_id))
        elif new_id is None:
            raise ValueError("Trying to assign id=None")

        self._id = new_id

    def has_computed_property(self,key):
        '''
        returns whether node has property methods that return dynamic values
        '''
        return key in self.get_computed_properties()

    @property
    def preview(self):
        return ""

    @property
    def id(self):
        return self.get_id()

    def get_id(self):
        return self._id

    def __getattr__(self, name):
        raise NotImplementedError()

    def get_type(self):
        return self.get_property("type")

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
    def graph(self):
        return self.get_graph()

    def get_graph(self) -> OpenKnowledgeGraph:
        return self._graph

    def __repr__(self):
        return "<Entity ({}): {}>".format(self.type, self.preview)

    def serialize(self):
        return None

    def matches(self, *queries, **query_args):
        return len(filter_entities([self], *queries, **query_args)) > 0

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    @staticmethod
    def get_computed_properties():
        return []

    @staticmethod
    def from_db_object():
        # TODO restore from database
        pass
