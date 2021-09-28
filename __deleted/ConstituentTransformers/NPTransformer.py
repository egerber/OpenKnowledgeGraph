from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.constituents.NPNode import NPNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.ConstituentTransformers.ConstituentListTransformer \
    import ConstituentListTransformer


class NPTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        self.np_list_transformer = ConstituentListTransformer(node_type="np")

    def apply(self, node, *args, **kwargs):
        if self.np_list_transformer.is_candidate(node):
            return self.np_list_transformer.apply(node)
        else:
            return NPNode.from_token_node(node)

    def get_pattern(self):
        #exclude conj -> is dealt with by listTransformer
        return Q(type="token", dep__in=["nsubj", "nsubjpass", "pobj", "dobj", "poss"]) | Q(
            pos__in=["noun", "propn", "pron"], dep__not="conj")

    @staticmethod
    def get_name():
        return "np"