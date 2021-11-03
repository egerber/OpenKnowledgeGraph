from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q


class TripletTransformer(GraphOperation):
    

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)
    

    def apply(self, node:Node, *args, **kwargs):
        predicate=node
        subject=node.find_out_nodes(type="constituent",dep="nsubj").first()
        object=node.find_out_nodes(type="constituent",dep="dobj").first()

        if subject and object:
            triplet_node=node.get_graph().create_node(node_type="triplet",properties={'tense':'past'})
            triplet_node.set_nested_property("subject",subject)
            triplet_node.set_nested_property("predicate",predicate)
            triplet_node.set_nested_property("object",object)

            return triplet_node

    @staticmethod
    def get_name():
        return "triplet"

    def get_pattern(self):
        return Q(type="canonical")
