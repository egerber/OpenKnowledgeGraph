from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.nodes.relations.InstanceOfRelation import InstanceOfRelation
from openKnowledgeGraph.queries.QuerySet import Q


class InstanceOfTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

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

    @staticmethod
    def get_name():
        return "instance_of"