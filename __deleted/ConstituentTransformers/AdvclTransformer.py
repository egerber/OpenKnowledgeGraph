from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.constituents.AdvclNode import AdvclNode
from openKnowledgeGraph.queries.QuerySet import Q


class AdvclTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="token", dep="advcl")

    def apply(self, node, *args, **kwargs):
        return AdvclNode.from_token_node(node)

    @staticmethod
    def get_name():
        return "advcl"