from openKnowledgeGraph.nodes.DependencyNode import DependencyNode


class DependencyNodeGroup(DependencyNode):

    def __init__(self, nodes):
        DependencyNode.__init__(self, nodes)

        self.nodes = nodes

    def get_text(self):
        return "<NodeGroup>"

    @staticmethod
    def get_type():
        return "node_group"
