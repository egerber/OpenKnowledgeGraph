from openKnowledgeGraph.nodes.Node import Node


class SpanNode(Node):

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    def get_start(self):
        pass

    def get_end(self):
        pass

    @property
    def start(self):
        return self.get_start()

    @property
    def end(self):
        return self.get_end()

    @staticmethod
    def from_root_token(token_node):
        pass
