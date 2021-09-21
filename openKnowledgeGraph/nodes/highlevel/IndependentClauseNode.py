from openKnowledgeGraph.nodes.Node import Node


class IndependentClauseNode(Node):
    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @staticmethod
    def get_type():
        return "independent_clause"

    @property
    def independent(self):
        return True

    @staticmethod
    def from_vp_node(vp_node):
        graph = vp_node.get_graph()
        ic_node = graph.create_reference_node(reference_node=vp_node,node_type="independent_clause")

        return ic_node
