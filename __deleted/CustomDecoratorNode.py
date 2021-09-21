from openKnowledgeGraph.nodes import DecoratorNode


class CustomDecoratorNode(DecoratorNode):
    def __init__(self, node_type, **kwargs):
        DecoratorNode.__init__(self, **kwargs)
        self.node_type = node_type

    def get_type(self):
        return self.node_type
