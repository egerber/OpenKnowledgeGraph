from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart


class AdjpNode(ConstituentNode):

    type="adjp"

    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)

    @staticmethod
    def from_token_node(token_node):
        graph = token_node.graph
        adjp_node = graph.create_node(node_type="adjp")
        graph.add_node(adjp_node)

        ConstituentNode.add_reference_link(adjp_node, token_node)
        ConstituentNode.link_constituents(adjp_node, token_node)

        return adjp_node
