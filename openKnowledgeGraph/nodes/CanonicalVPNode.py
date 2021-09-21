from openKnowledgeGraph.nodes import VPNode


class CanonicalVPNode(VPNode):

    type="canonical_vp"
    
    def __init__(self, **kwargs):
        VPNode.__init__(self, **kwargs)
