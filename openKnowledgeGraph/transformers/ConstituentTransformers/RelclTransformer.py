from openKnowledgeGraph.nodes.constituents.VPNode import VPNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer

REFERENCE_WORDS_SUBJ = ["that", "who", "which", "where"]


class RelclTransformer(NodeTransformer):
    '''
    converts relative clause (the woman, who wore the red dress, went away) -> the woman wore a red dress
    '''

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def apply(self, node, *args, **kwargs):
        return VPNode.from_token_node(token_node=node, override_deps=None)

        parent = node.find_in_nodes(type="token").first()

        subject_node = node.find_out_nodes(type="token", dep__in=["nsubj", "nsubjpass"]).first()
        object_node = node.find_out_nodes(type="token", dep__in=["dobj", "pobj"]).first()

        override_deps = {}

        if parent:
            if subject_node is None or subject_node.text in REFERENCE_WORDS_SUBJ:
                subject_node = parent
            elif object_node is None or object_node.text in REFERENCE_WORDS_SUBJ:
                subject_node = parent

        if subject_node:
            if subject_node.dep.startswith('nsubj'):
                subject_dep = subject_node.dep
            else:
                subject_dep = "nsubj"  # sometimes the subject is inherited from dep=attr
            override_deps[subject_dep] = subject_node
        if object_node:
            override_deps[object_node.dep] = object_node
        return VPNode.from_token_node(token_node=node, override_deps=override_deps)

    def get_pattern(self):
        return Q(type="token", dep="relcl")
