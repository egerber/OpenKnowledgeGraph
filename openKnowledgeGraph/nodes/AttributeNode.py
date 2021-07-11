from openKnowledgeGraph.nodes.DependencyNode import DependencyNode


class AttributeDependencyNode(DependencyNode):

    def __init__(self, customDependencyNode):
        DependencyNode.__init__(self, customDependencyNode)

    def get_text(self):
        return self.customDependencyNode.text

    @staticmethod
    def get_type():
        return "attribute"

    @staticmethod
    def from_dependency_node(custom_dependency_node):
        return AttributeDependencyNode(custom_dependency_node)
