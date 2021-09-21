from openKnowledgeGraph.links.BroadcastLink import BroadcastLink
from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.nodes.DependencyNode import DependencyNode
from openKnowledgeGraph.nodes.objects.ObjectNode import ObjectDependencyNode


class ListNode(ConstituentNode):

    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)

    def get_text(self):
        return "<List: {}>".format(super().get_text())

    def create_links(self):
        links = super().create_links()

        return links

    @staticmethod
    def get_type():
        return "list"
