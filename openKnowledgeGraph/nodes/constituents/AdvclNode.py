from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.nodes.constituents.VPNode import VPNode


class AdvclNode(VPNode):

    def __init__(self, **kwargs):
        VPNode.__init__(self, **kwargs)\

    @staticmethod
    def get_type():
        return "advcl"

    def get_mark(self):
        return self.reference.find_out_nodes(type="token", dep="mark").first()

    @staticmethod
    def from_token_node(token_node, override_deps=None):
        graph = token_node.graph

        advcl_node = AdvclNode()
        graph.add_node(advcl_node)

        ConstituentNode.add_reference_link(advcl_node, token_node)
        ConstituentNode.link_constituents(constituent_node=advcl_node,
                                          token_node=token_node,
                                          override_deps=override_deps)

        return advcl_node
