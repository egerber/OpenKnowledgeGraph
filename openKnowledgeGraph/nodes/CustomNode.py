from openKnowledgeGraph.nodes.Node import Node


class CustomNode(Node):

    def __init__(self, node_type, **kwargs):
        Node.__init__(self, **kwargs)
        self.node_type = node_type

    def get_type(self):
        return self.node_type
