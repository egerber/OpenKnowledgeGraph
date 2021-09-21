from openKnowledgeGraph.nodes.Node import Node


class DependencyNode(Node):

    type="dependency"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)