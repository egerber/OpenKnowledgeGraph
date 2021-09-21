from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart


class AdvpNode(ConstituentNode):

    type="advp"
    
    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)

    @staticmethod
    def from_token_node(token_node):
        graph = token_node.graph
        advp_node = graph.create_node(node_type="advp")
        graph.add_node(advp_node)
        ConstituentNode.add_reference_link(advp_node, token_node)
        ConstituentNode.link_constituents(advp_node, token_node)

        return advp_node
