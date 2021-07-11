from openKnowledgeGraph.nodes.ReferenceNode import ReferenceNode


class IndependentClauseNode(ReferenceNode):
    def __init__(self, **kwargs):
        ReferenceNode.__init__(self, **kwargs)

    @staticmethod
    def get_type():
        return "independent_clause"

    @property
    def independent(self):
        return True

    @staticmethod
    def from_vp_node(vp_node):
        graph = vp_node.get_graph()
        ic_node = IndependentClauseNode()
        graph.add_node(ic_node)
        ReferenceNode.create_reference_link(ic_node, vp_node)

        return ic_node
