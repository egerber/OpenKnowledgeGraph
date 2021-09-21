from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.queries.QuerySet import Q


class DecoratorNode(Node):
    '''
    inherits attributes and behaviour of other node
    allows to attach more attributes and override behaviour
    '''

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @property
    def core(self):
        return self.get_core()

    def get_core(self):
        return self.find_out_links(Q(type="decorator")).first().target

    def __repr__(self):
        return "<Decorator {}: {}: {}>".format(self.core.__repr__(), self.get_type(), self.get_text())

    @staticmethod
    def create_decorator_link(decorator_node, target_node):
        graph = decorator_node.graph

        graph.create_link("decorator", decorator_node, target_node)
