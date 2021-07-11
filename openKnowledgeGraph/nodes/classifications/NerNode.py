from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.DecoratorNode import DecoratorNode
from openKnowledgeGraph.queries.QuerySet import Q


class NerNode(DecoratorNode):

    def __init__(self, label=None, **kwargs):
        DecoratorNode.__init__(self, **kwargs)
        self._label = label

    @property
    def ner(self):
        return self._label

    def get_text(self):
        return "{} ({})".format(self.core.type, self.ner)

    @property
    def label(self):
        return self._label

    @staticmethod
    def get_type():
        return "ner"

    @staticmethod
    def create_for_core_node(core_node, label):
        graph = core_node.get_graph()
        ner_node = NerNode(label=label)
        graph.add_node(ner_node)
        graph.add_link(Link.create("decorator", ner_node, core_node))

        return ner_node
