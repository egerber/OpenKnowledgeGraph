from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class TripleTemplateTransformer(NodeTransformer):
    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="vp")

    def apply(self, node, *args, **kwargs):
        pass
