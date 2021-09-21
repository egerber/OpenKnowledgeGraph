from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q


class TripleTemplateTransformer(GraphOperation):
    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="vp")

    def apply(self, node, *args, **kwargs):
        pass
