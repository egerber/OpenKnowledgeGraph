import itertools
from openKnowledgeGraph import nodes

from openKnowledgeGraph.nodes import CanonicalVPNode, Node
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q


class CanonicalizationTransformer(GraphOperation):

    def __init__(self, canonicalize_properties=None, resolve_corefs=True, resolve_relcls=True, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        #self.consituent_list_transformer=ConstituentListTransformer2()

    def get_pattern(self):
        return Q(type="constituent",constituent_type="vp", dep="root")

    def get_list_elements(self,node:Node):
        coordination_selection = node.traverse_graph_by_out_links(
            query=Q(type="constituent", dep__in=["conj", "cc"])
        ).filter_links(dep__not="cc")

        coordination_nodes=coordination_selection.nodes

        cloned_coordination_elements=[]
        for coordination_element in coordination_nodes:
            cloned_constituent_subtree=coordination_element \
                .traverse_graph_by_out_links(
                    query=Q(type="constituent",dep__not="cc",id__nin=coordination_selection.links.id)
                ).clone_with_references()
            
            cloned_root_constituent=cloned_constituent_subtree.nodes.first()
            cloned_coordination_elements.append(cloned_root_constituent)

        return cloned_coordination_elements


    def apply(self, vp_node:Node, subject=None,*args, **kwargs):
        children=vp_node.get_children()
        child_deps=children.dep
        if not ("nsubj" in child_deps or "nsubjpass" in child_deps) \
            and subject is not None: #and vp_node does not have subject
            children.append(subject)

        exploded_children=[]
        canonical_nodes=[]

        subject=vp_node.find_out_nodes(type="constituent",dep__in=["nsubj","nsubjpass"]).first()

        if vp_node.is_coordination:
            vp_list_elements=self.get_list_elements(vp_node)
            for vp_list_element in vp_list_elements:
                canonical_nodes+=self.apply(vp_list_element,subject=subject)
        else:
            for child in children:
                if child.is_coordination:
                    exploded_children.append(self.get_list_elements(child))
                elif child.dep=="relcl":
                    self.apply(child,subject=subject)
                else:
                    exploded_children.append([child])
        
            for canonical_children in itertools.product(*exploded_children):
                canonical_node=vp_node.get_graph().create_reference_node(reference_node=vp_node, node_type="canonical")
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
        return ["constituent"]

    @staticmethod
    def get_name():
        return "canonical"