from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.constituents.VPNode import VPNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.ConstituentTransformers.RelclTransformer import \
    RelclTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.ConstituentListTransformer import \
    ConstituentListTransformer


class VPTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        self.relcl_transformer = RelclTransformer()
        self.vp_list_transformer = ConstituentListTransformer(node_type="vp")

    def apply(self, node, *args, **kwargs):
        if self.relcl_transformer.is_candidate(node):
            return self.relcl_transformer.apply(node)
        elif self.vp_list_transformer.is_candidate(node):
            return self.vp_list_transformer.apply(node)
        else:
            return VPNode.from_token_node(node)

    def get_pattern(self):
        return Q(type="dependency", dep__in=["root", "ccomp", "relcl", "xcomp", "advcl"]) | Q(pos__in=["verb"],
                                                                                         dep__not="conj") | Q(dep__not="conj",pos="aux",
                                                                                                              lemma="be")  # TODO later add support for xcomp

    @staticmethod
    def get_name():
        return "vp"