from openKnowledgeGraph.nodes.relations.InstanceOfRelation import InstanceOfRelation
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class InstanceOfTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="triplet",
                 custom=lambda triplet: triplet.predicate.lemma == "be" and triplet.object.dep == "attr")

    def find_candidate_nodes(self, graph):
        return graph.find_nodes(type="triplet").filter(
            custom=lambda triplet: triplet.predicate.lemma == "be" and triplet.object.dep == "attr")

    def apply(self, node, *args, **kwargs):
        entity = node.subject
        group = node.object

        return InstanceOfRelation.from_arguments(entity=entity, group=group)
