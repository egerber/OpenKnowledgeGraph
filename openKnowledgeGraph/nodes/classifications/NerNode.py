from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.queries.QuerySet import Q


class NerNode(Node):

    type="ner"

    def __init__(self, label=None, **kwargs):
        Node.__init__(self, **kwargs)
        self._label = label

    @property
    def ner(self):
        return self._label

    def get_text(self):
        return "{} ({})".format(self.core.type, self.ner)

    @property
    def label(self):
        return self._label