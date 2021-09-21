from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.nodes.constituents.VPNode import VPNode


class SbarNode(VPNode):

    type="sbar"

    def __init__(self, **kwargs):
        VPNode.__init__(self, **kwargs)

    def get_mark(self):
        return self.reference.find_out_nodes(type="token", dep="mark").first()

    @staticmethod
    def from_token_node(token_node, override_deps=None):
        graph = token_node.graph

        sbar_node = graph.create_node(node_type="sbar")
        graph.add_node(sbar_node)

        ConstituentNode.add_reference_link(sbar_node, token_node)
        ConstituentNode.link_constituents(constituent_node=sbar_node,
                                          token_node=token_node,
                                          override_deps=override_deps)

        return sbar_node
