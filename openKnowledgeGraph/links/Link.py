from openKnowledgeGraph.Entity import Entity
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class Link(Entity):

    def __init__(self, source_id, target_id, **kwargs):
        Entity.__init__(self, **kwargs)
        self._source_id = source_id
        self._target_id = target_id

        for attr_name, attr_value in kwargs.items():
            self.attributes[attr_name] = attr_value

    def get_source_id(self):
        return self._source_id

    def get_target_id(self):
        return self._target_id

    def set_property(self,key,value):
        self.graph.set_property_for_link(self.id,key,value)

    def get_property(self,key):
        return self.graph.get_property_for_link(self.id,key)

    def has_property(self,key):
        return self.graph.link_has_property(self.id,key)

    @property
    def target_id(self):
        return self._target_id

    @property
    def source_id(self):
        return self._source_id

    @property
    def source(self):
        return self.get_source()

    @property
    def target(self):
        return self.get_target()

    def get_source(self):
        return self.get_graph().get_node(self.get_source_id())

    def get_target(self):
        return self.get_graph().get_node(self.get_target_id())

    @staticmethod
    def get_type():
        return "link"

    def __repr__(self):
        if self.get_graph() is not None:
            return "Link:{}<{},{}>".format(self.get_type(), self.get_source(), self.get_target())
        else:
            return "Link:{}<id:{},id:{}>".format(self.get_type(), self.get_source_id(), self.get_target_id())

    def clone_with_properties(self, source_id, target_id):
        return type(self)(source_id, target_id)

    def serialize(self):
        return {
            "id": self.get_id(),
            "type": self.get_type(),
            "src": self.get_source_id(),
            "target": self.get_target_id()
        }


    def set_property(self,key,value):
        self.graph.set_property_for_link(self.id,key,value)

    def get_property(self,key):
        return self.graph.get_property_for_link(self.id,key)

    def has_property(self,key):
        return self.graph.link_has_property(self.id,key)

    def __getattr__(self, name):
        if self.has_property(name):
            return self.get_property(name)
        else:
            try:
                return self.__getattribute__(name)
            except:
                return None


    @staticmethod
    def create(type, source, target, **kwargs):
        LinkClass = LinkRegistry.get_by_type(type)

        if source is None:
            raise ValueError("source is None")
        if target is None:
            raise ValueError("target is None")

        if not source.has_id():
            raise ValueError(
                "Cannot add link: source has has no id (probably because it was not yet added to the KnowledgeGraph)")
        if not target.has_id():
            raise ValueError(
                "Cannot add link: target has has no id (probably because it was not yet added to the KnowledgeGraph)")

        if LinkClass is not None:
            return LinkClass(source.get_id(), target.get_id(), **kwargs)
        else:
            from openKnowledgeGraph.links.CustomLink import CustomLink
            return CustomLink(type, source_id=source.get_id(), target_id=target.get_id(), **kwargs)
