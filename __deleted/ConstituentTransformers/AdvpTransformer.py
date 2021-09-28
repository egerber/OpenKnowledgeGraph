from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.constituents.AdvpNode import AdvpNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.ConstituentTransformers.ConstituentListTransformer import ConstituentListTransformer


class AdvpTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        self.advp_list_transformer = ConstituentListTransformer(node_type="advp")

    def is_candidate(self, node):
        return node.matches(Q(type="token", dep="advmod") & Q(pos__in=["adv", "adj"], dep__not="conj"))

    def apply(self, node, *args, **kwargs):
        if self.advp_list_transformer.is_candidate(node):
            return self.advp_list_transformer.apply(node)
        else:
            return AdvpNode.from_token_node(node)

    @staticmethod
    def get_name():
        return "advp"