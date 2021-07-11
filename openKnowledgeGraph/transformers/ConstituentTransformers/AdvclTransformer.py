from openKnowledgeGraph.nodes.constituents.AdvclNode import AdvclNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class AdvclTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="token", dep="advcl")

    def apply(self, node, *args, **kwargs):
        return AdvclNode.from_token_node(node)
