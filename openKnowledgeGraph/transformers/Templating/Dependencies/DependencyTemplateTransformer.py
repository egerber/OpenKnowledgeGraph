from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.Template import Template
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class DependencyTemplateTransformer(NodeTransformer):

    def __init__(self, max_dept=5,**kwargs):
        NodeTransformer.__init__(self,**kwargs)


    def get_pattern(self):
        return Q(type="vp")

    def apply(self,node):
        template=Template(value=node) #needs to

        for child in node.find_out_links(type="constituent").targets:
