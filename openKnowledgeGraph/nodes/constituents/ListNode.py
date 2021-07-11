from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.queries.QuerySet import Q


class ListNode(ConstituentNode):

    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)

    @staticmethod
    def add_list_elements(list_node):
        graph = list_node.get_graph()

        conj_deps = list_node.get_reference().traverse_by_out_links(
            query=Q(type="dependency", attr__dependency_type="conj"))

        for conj_dep in conj_deps:
            graph.add_link(Link.create("list_element", list_node, conj_dep))

    @staticmethod
    def get_type():
        return "list"
