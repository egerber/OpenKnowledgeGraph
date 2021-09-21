from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.nodes.NoneNode import NoneNode


class RelationNode(Node):

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    def find_argument(self, type):
        outlinks = self._get_out_links_list(type="argument", argument_type=type)
        if len(outlinks) > 0:
            return outlinks[0].target
        else:
            return NoneNode.create_for_node(self)

    @staticmethod
    def from_relation():
        # set argument links
        pass