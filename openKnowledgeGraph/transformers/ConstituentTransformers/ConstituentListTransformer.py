from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.nodes import ConstituentNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation


class ConstituentListTransformer(GraphOperation):
    '''
    analyzes conjunctions (x and y, ...) in the dependency tree and references them as 
    '''

    def __init__(self, node_type=None, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        if node_type is None:
            raise ValueError("need to specify node_type for ConstituentListTransformer")
        self.node_type = node_type

    def get_pattern(self):
        return Q(type="token", custom=lambda node: node.find_out_nodes(type="token", dep="conj"))

    def apply(self, node, *args, **kwargs):
        list_elements = node.traverse_by_out_links(
            query=Q(type="dependency", dependency_type="conj"))
        elements = []

        list_constituents = []
        for list_element in list_elements:
            list_element_constituent = ConstituentListTransformer.create_list_element(
                node_type=self.node_type,
                list_element=list_element
            )
            elements.append(list_element_constituent)
            list_constituents.append(list_element_constituent)

        elements.append(ConstituentListTransformer.create_from_list_elements(
            node_type=self.node_type, root_node=node,
            list_elements=list_constituents)
        )
        
        
        return elements

    @staticmethod
    def create_list_element(node_type, list_element):
        graph = list_element.get_graph()
        np_node = graph.create_reference_node(
            reference_node=list_element,
            node_type=node_type, 
            properties={'is_list_element':True})

        ConstituentNode.link_constituents(np_node, list_element, 
            override_deps={
                'conj': None,
                'cc': None
            }
        )
        

        return np_node

    @staticmethod
    def create_from_list_elements(node_type:str, root_node:Node, list_elements):
        graph = root_node.get_graph()

        list_root_constituent = graph.create_reference_node(reference_node=root_node, node_type=node_type)
        for list_element in list_elements:
            graph.create_link('list', list_root_constituent, list_element)

        coordination_elements = root_node.traverse_by_out_links(
            query=Q(type="dependency", dependency_type__in=["conj", "cc"])).filter(dep="cc")
        
        for cc in coordination_elements:
            graph.create_link('constituent', list_root_constituent, cc, constituent_type="leaf")


        return list_root_constituent

    @staticmethod
    def get_name():
        return "constituent_list"