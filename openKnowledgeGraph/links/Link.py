from openKnowledgeGraph.Entity import Entity
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class Link(Entity):

    def __init__(self,**kwargs):
        Entity.__init__(self, **kwargs)
      
    def set_property(self,key,value):
        self.graph.set_property_for_link(self.id,key,value)

    def get_property(self,key):
        return self.graph.get_property_for_link(self.id,key)

    def has_property(self,key):
        return self.graph.link_has_property(self.id,key)

    def get_properties(self) -> dict:
        return self.graph.get_properties_for_link(self.get_id())

    @property
    def source(self):
        return self.get_source()

    @property
    def target(self):
        return self.get_target()

    def get_source(self):
        return self.get_graph().get_node(self.source_id)

    def get_target(self):
        return self.get_graph().get_node(self.target_id)

    def __repr__(self):
        if self.get_graph() is not None:
            return "Link:{}<{},{}>".format(self.get_type(), self.get_source(), self.get_target())

    def clone_with_properties(self, source_id, target_id):
        return type(self)(source_id, target_id)

    def set_property(self,key,value):
        self.graph.set_property_for_link(self.id,key,value)

    def get_property(self,key):
        return self.graph.get_property_for_link(self.id,key)

    def has_property(self,key):
        return self.graph.link_has_property(self.id,key)