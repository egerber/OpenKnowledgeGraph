from openKnowledgeGraph.links.AmodLink import AmodLink
from openKnowledgeGraph.links.ObjectPrepositionLink import ObjectPrepositionLink
from openKnowledgeGraph.links.PossLink import PossLink
from openKnowledgeGraph.nodes.DependencyNode import DependencyNode


# should be more something like Object Node
class ObjectDependencyNode(DependencyNode):

    def __init__(self, custom_dependency_node, preps=[], amods=[], poss=None):
        DependencyNode.__init__(self, customDependencyNode=custom_dependency_node)
        self.preps = preps
        self.amods = amods
        self.poss = poss
        self.node = custom_dependency_node

    def create_links(self):
        links = []
        for prep in self.preps:
            core_arg = prep.get_core_argument()
            if core_arg is not None:
                links.append(
                    ObjectPrepositionLink(self.get_id(), core_arg.get_id()))
        for amod in self.amods:
            links.append(AmodLink(self.get_id(), amod.get_id()))

        if self.poss is not None:
            links.append(PossLink(self.get_id(), self.poss.get_id()))

        return links

    def get_text(self):
        return self.get_dependency_node().text

    @staticmethod
    def get_type():
        return "object"

    @staticmethod
    def from_dependency_node(custom_dependency_node, preps, amods, poss):
        return ObjectDependencyNode(custom_dependency_node, preps, amods, poss)
