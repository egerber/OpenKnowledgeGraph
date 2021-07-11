from openKnowledgeGraph.links.CorefLink import CorefLink
from openKnowledgeGraph.nodes.objects.ObjectNode import ObjectDependencyNode


class CorefNode(ObjectDependencyNode):

    def __init__(self, custom_dependency_node, coref, preps=[], amods=[]):
        ObjectDependencyNode.__init__(self, custom_dependency_node=custom_dependency_node, preps=preps, amods=amods)
        self.node = custom_dependency_node
        self.coref = coref

    def get_text(self):
        return self.node.text

    def create_links(self):
        links = super().create_links()
        links += [CorefLink(self.node.get_id(), self.coref.get_id())]

        return links

    def _get_out_links_list(self):
        return [self.coref]

    @staticmethod
    def get_type():
        return "coref"

    @staticmethod
    def from_dependency_node(custom_dependency_node, coref, preps=[], amods=[]):
        return CorefNode(custom_dependency_node, coref, preps, amods)
