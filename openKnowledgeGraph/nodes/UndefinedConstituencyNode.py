from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode


class UndefinedConstituencyNode(ConstituentNode):

    def __init__(self, custom_constituency_node):
        ConstituentNode.__init__(self, constituency_node=custom_constituency_node)

    @staticmethod
    def get_type():
        return "undefined_node"
