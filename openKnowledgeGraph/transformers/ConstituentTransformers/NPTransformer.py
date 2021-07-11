from openKnowledgeGraph.nodes.constituents.NPNode import NPNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.ConstituentListTransformer \
    import ConstituentListTransformer


class NPTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)
        self.np_list_transformer = ConstituentListTransformer(node_type="np")

    def apply(self, node, *args, **kwargs):
        if self.np_list_transformer.is_candidate(node):
            return self.np_list_transformer.apply(node)
        else:
            return NPNode.from_token_node(node)

    def get_pattern(self):
        return Q(type="token", dep__in=["nsubj", "nsubjpass", "pobj", "dobj", "poss"]) | Q(
            pos__in=["noun", "propn", "pron"], dep__not="conj")
