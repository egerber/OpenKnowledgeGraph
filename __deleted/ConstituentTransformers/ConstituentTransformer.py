from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.ConstituentTransformers.AdjpTransformer import \
    AdjpTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.AdvclTransformer import \
    AdvclTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.AdvpTransformer import \
    AdvpTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.NPTransformer import NPTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.PPTransformer import PPTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.SbarTransformer import \
    SbarTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.VPTransformer import VPTransformer


class ConstituentTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        self.advcl_transformer = AdvclTransformer()
        self.np_transformer = NPTransformer()
        self.pp_transformer = PPTransformer()
        self.advp_transformer = AdvpTransformer()
        self.vp_transformer = VPTransformer()
        self.sbar_transformer = SbarTransformer()
        self.adjp_transformer = AdjpTransformer()

    def apply(self, node, *args, **kwargs):
        # returns traversed tree ordered from leaves to root
        traversed_nodes = node.traverse_by_out_links(max_depth=100, query=Q(type="dependency")).reverse()
        for token in traversed_nodes:
            if self.advcl_transformer.is_candidate(token):
                self.advcl_transformer.apply(token)
            elif self.sbar_transformer.is_candidate(token):
                self.sbar_transformer.apply(token)
            elif self.np_transformer.is_candidate(token):
                self.np_transformer.apply(token)
            elif self.pp_transformer.is_candidate(token):
                self.pp_transformer.apply(token)
            elif self.advp_transformer.is_candidate(token):
                self.advp_transformer.apply(token)
            elif self.vp_transformer.is_candidate(token):
                self.vp_transformer.apply(token)
            elif self.adjp_transformer.is_candidate(token):
                self.adjp_transformer.apply(token)
            else:
                print("no logic for node")
    
    @staticmethod
    def get_name():
        return "constituent"

    def get_pattern(self):
        return Q(type="dependency", dep="root")
