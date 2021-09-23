import itertools
from openKnowledgeGraph import nodes

from openKnowledgeGraph.nodes import CanonicalVPNode, Node
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q


class CanonicalizationTransformer2(GraphOperation):

    def __init__(self, canonicalize_properties=None, resolve_corefs=True, resolve_relcls=True, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        #self.consituent_list_transformer=ConstituentListTransformer2()

    def get_pattern(self):
        return Q(type="constituent2",constituent_type="vp", dep="root")

    def get_list_elements(self,node:Node):
        coordination_elements = node.traverse_by_out_links(
            query=Q(type="constituent", dep__in=["conj", "cc"])).filter(dep__not="cc")

        return coordination_elements

    def apply(self, vp_node:nodes, *args, **kwargs):
        children=vp_node.get_children()

        exploded_children=[]

        for child in children:
            if child.is_coordination:
                exploded_children.append(self.get_list_elements(child))
            else:
                exploded_children.append([child])
        
        canonical_nodes=[]
        for canonical_children in itertools.product(*exploded_children):
            canonical_node=vp_node.get_graph().create_reference_node(reference_node=vp_node, node_type="canonical2")
            for child in canonical_children:
                vp_node.get_graph().create_link(
                    link_type="constituent",
                    source=canonical_node,
                    target=child,
                    dep=child.dep
                )
            canonical_nodes.append(canonical_node)
        
        return canonical_nodes
            

    @staticmethod
    def get_dependencies():
        return ["dependency","constituent2"]

    @staticmethod
    def get_name():
        return "canonical2"