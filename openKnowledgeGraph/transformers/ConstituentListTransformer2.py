from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.nodes import ConstituentNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation


class ConstituentListTransformer2(GraphOperation):
    '''
    analyzes conjunctions (x and y, ...) in the dependency tree and references them as 
    '''

    def __init__(self, node_type=None, **kwargs):
        GraphOperation.__init__(self, **kwargs)
       

    def get_pattern(self):
        return Q(type="constituent2",is_coordination=True)

    def apply(self, node, *args, **kwargs):
        pass
