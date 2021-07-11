from openKnowledgeGraph.nodes.classifications.PPTypeNode import PPTypeNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class PPTypeTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="pp")

    def apply(self, node,*args,**kwargs):
        prep_object = node.object

        label = None
        if prep_object:
            if prep_object.ner == "date":
                label = "date"
            elif prep_object.ner == "time":
                label = "time"

        if label is not None:
            return PPTypeNode.from_pp_node(pp_node=node, label=label)
