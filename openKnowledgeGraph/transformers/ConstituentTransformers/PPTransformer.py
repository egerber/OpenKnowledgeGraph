from openKnowledgeGraph.nodes.constituents.PPNode import PPNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class PPTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def apply(self, node, *args, **kwargs):
        return PPNode.from_token_node(node)

    def get_pattern(self):
        return Q(type="token", dep__in=["prep", "agent"])
