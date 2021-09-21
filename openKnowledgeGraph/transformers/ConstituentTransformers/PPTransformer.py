from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.constituents.PPNode import PPNode
from openKnowledgeGraph.queries.QuerySet import Q


class PPTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def apply(self, node, *args, **kwargs):
        return PPNode.from_token_node(node)

    def get_pattern(self):
        return Q(type="token", dep__in=["prep", "agent"])
    
    @staticmethod
    def get_name():
        return "pp"