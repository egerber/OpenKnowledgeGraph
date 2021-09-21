from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.highlevel.IndependentClauseNode import IndependentClauseNode
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.queries.QuerySet import Q


class IndependentClauseTransformer(GraphOperation):
    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    @staticmethod
    def get_name():
        return "IndependentClauseTransformer"

    def get_pattern(self):
        return Q(type__in=["advcl", "vp", "sbar"],
                 custom=lambda node: node.find_child_by_type("nsubj") or node.find_child_by_type("nsubjpass"))

    def apply(self, node, *args, **kwargs):
        return IndependentClauseNode.from_vp_node(node)
