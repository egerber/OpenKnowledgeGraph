from openKnowledgeGraph.nodes.Node import Node


class NoneNode(Node):
    
    type="none"

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    def get_text(self):
        return None

    def __getattr__(self, item):
        return None

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

    @staticmethod
    def create_for_node(node):
        none_node = NoneNode(graph=node.get_graph())

        return none_node
