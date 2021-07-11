from openKnowledgeGraph.nodes import VPNode


class CanonicalVPNode(VPNode):

    def __init__(self, **kwargs):
        VPNode.__init__(self, **kwargs)

    @staticmethod
    def get_type():
        return "canonical_vp"
