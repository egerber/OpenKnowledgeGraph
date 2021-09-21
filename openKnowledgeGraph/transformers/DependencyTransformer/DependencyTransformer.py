from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q


class DependencyTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def apply(self, node: Node, *args, **kwargs):
        dependency_node=node.graph.create_reference_node(reference_node=node,node_type="dependency",properties={})

        traversed_nodes = node.traverse_by_out_links(max_depth=100, query=Q(type="dependency"))[1:].reverse()
        for token in traversed_nodes:
            node.graph.create_link(link_type="dependency",source=dependency_node, target=self.apply(token),dep=token.dep)
    
        return dependency_node

    @staticmethod
    def get_name():
        return "dependency"

    @staticmethod
    def get_dependencies():
        return ["token"]

    def get_pattern(self):
        return Q(type="token", dep="root")