from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.constituents.SbarNode import SbarNode
from openKnowledgeGraph.queries.QuerySet import Q


class SbarTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="token", dep="ccomp")

    def apply(self, node, *args, **kwargs):
        return SbarNode.from_token_node(node)

    @staticmethod
    def get_name():
        return "sbar"