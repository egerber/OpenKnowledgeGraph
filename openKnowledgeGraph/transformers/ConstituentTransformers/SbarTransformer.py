from openKnowledgeGraph.nodes.constituents.SbarNode import SbarNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class SbarTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="token", dep="ccomp")

    def apply(self, node, *args, **kwargs):
        return SbarNode.from_token_node(node)
