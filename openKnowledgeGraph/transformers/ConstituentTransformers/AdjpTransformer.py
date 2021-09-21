from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.constituents.AdjpNode import AdjpNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.ConstituentTransformers.ConstituentListTransformer import \
    ConstituentListTransformer


class AdjpTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        self.adjp_list_transformer = ConstituentListTransformer(node_type="adjp")

    def get_pattern(self):
        return Q(type="token", dep__not="conj") & (Q(dep="acomp") | Q(pos="adj"))

    def apply(self, node, *args, **kwargs):
        if self.adjp_list_transformer.is_candidate(node):
            return self.adjp_list_transformer.apply(node)
        else:
            return AdjpNode.from_token_node(node)
    
    @staticmethod
    def get_name():
        return "adjp"