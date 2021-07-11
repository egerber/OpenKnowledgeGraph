from openKnowledgeGraph.nodes.DecoratorNode import DecoratorNode


class PPTypeNode(DecoratorNode):
    def __init__(self, label=None, **kwargs):
        DecoratorNode.__init__(self, **kwargs)
        self._label = label

    def get_label(self):
        return self._label

    @property
    def label(self):
        return self.get_label()

    @staticmethod
    def get_type():
        return "pp_type"

    @staticmethod
    def from_pp_node(pp_node, label):
        graph = pp_node.graph
        
        pp_type_node = PPTypeNode(label=label)
        graph.add_node(pp_type_node)
        DecoratorNode.create_decorator_link(pp_type_node, pp_node)
