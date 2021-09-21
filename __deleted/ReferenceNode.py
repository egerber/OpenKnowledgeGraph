from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.Node import Node


class ReferenceNode(Node):
    '''
    inherits attributes from referenced node
    '''
    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @staticmethod
    def get_type():
        return "reference"

    @property
    def reference(self):
        return self.get_reference()

    def get_reference(self):
        return self.find_out_links(type="reference").first().target

    def get_property(self,name):
        if super().has_property(name):
            return super().get_property(name)
        else:
            return self.get_reference().get_property(name)


    def __getattr__(self, item):
        own_attribute = super().__getattr__(item)
        if own_attribute:
            return own_attribute
        else:
            return self.get_reference().__getattr__(item)

    @staticmethod
    def create_reference_link(source_node, target_node):
        graph = source_node.get_graph()
        graph.create_link("reference", source_node, target_node)