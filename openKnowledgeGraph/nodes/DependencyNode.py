# hyper node should be only used to convert data of a specific type into the graph representation
from openKnowledgeGraph.nodes.Node import Node

class DependencyNode(Node):
    # node is always passed as reference to original customDependencyNode
    def __init__(self, customDependencyNode):
        Node.__init__(self)
        self.properties = {}
        self.customDependencyNode = customDependencyNode

    def get_dependency_node(self):
        return self.customDependencyNode

    def get_id(self):
        return self.customDependencyNode.get_id()

    def get_text(self):
        return self.get_dependency_node().text

    def get_property(self, property_name):
        self.properties.get(property_name, None)

    def get_node_connections(self):
        connections = []
        for link in self._get_in_links_list():
            connections.append((link.get_id(), self.get_id()))
        for link in self._get_out_links_list():
            connections.append((self.get_id(), link.get_id()))

        return connections

    @staticmethod
    def get_type():
        return "dependency"

    @staticmethod
    def from_tokens(token, preps=[]):
        pass
