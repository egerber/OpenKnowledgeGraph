class NodeRegistry:
    NodeTypes = {}

    @staticmethod
    def register_node(node_type: str, node_class):
        NodeRegistry.NodeTypes[node_type] = node_class

    @staticmethod
    def get_by_type(node_type):
        if node_type in NodeRegistry.NodeTypes:
            return NodeRegistry.NodeTypes[node_type]
        else:
            return None
