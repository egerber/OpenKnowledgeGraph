from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode

from openKnowledgeGraph.templates.TextPart import TextPart


class PPNode(ConstituentNode):

    name="pp"

    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)

    @property
    def object(self):
        return self.get_object()

    def get_object(self):
        return self.find_child_by_type("object")

    @property
    def preposition(self):
        return self.get_preposition()

    def get_preposition(self):
        return self.find_child_by_type("preposition")

    @staticmethod
    def from_token_node(token_node):
        graph = token_node.get_graph()
        pp_node = graph.create_node("pp",properties={"reference_node":token_node})
        graph.add_node(pp_node)

        ConstituentNode.add_reference_link(pp_node, token_node)
        ConstituentNode.link_constituents(pp_node, token_node)

        return pp_node
