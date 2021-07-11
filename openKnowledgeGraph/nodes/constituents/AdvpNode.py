from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart


class AdvpNode(ConstituentNode):

    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)

    @staticmethod
    def get_type():
        return "advp"

    @staticmethod
    def from_token_node(token_node):
        graph = token_node.graph
        advp_node = AdvpNode()
        graph.add_node(advp_node)
        ConstituentNode.add_reference_link(advp_node, token_node)
        ConstituentNode.link_constituents(advp_node, token_node)

        return advp_node
