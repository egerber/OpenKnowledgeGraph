from __future__ import annotations
from typing import Dict, List, Tuple
import itertools
from openKnowledgeGraph import nodes
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.nodes import CanonicalVPNode
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q


class CanonicalizationTransformer(GraphOperation):

    def __init__(self, canonicalize_properties=None, resolve_corefs=True, resolve_relcls=True, **kwargs):
        GraphOperation.__init__(self, **kwargs)

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
                ) \
                .clone_with_references()
            
            cloned_root_constituent=cloned_constituent_subtree.nodes.first()
            cloned_coordination_elements.append(cloned_root_constituent)

        return cloned_coordination_elements

    def get_canonicalized_vps_from_np(self, np:Node) -> Tuple[Node, List[Node]]:
        canonicalized_np=np
        canonical_vps=[]
        
        canonicalized_children=[]
        ignore_children=[]
        relcls=[]
        attrs=[]

        has_nested_vp_node=False
        for child in np.get_children():
            if child.dep=="relcl":
                has_nested_vp_node=True
                relcls.append(child)
                ignore_children.append(child)
            elif child.dep=="punct": #maybe too restrictive
                ignore_children.append(child)
            elif child.dep=="attr":
                ignore_children.append(child) 
            else: 
                canonicalized_children.append(child)

        if has_nested_vp_node:
            cloned_subgraph=np.traverse_graph_by_out_links(
                    query=Q(type="constituent",target_id__nin=[child.id for child in ignore_children])
                )
            cloned_subgraph=cloned_subgraph.clone_with_references()
            canonicalized_np=cloned_subgraph.nodes.first()

        for relcl in relcls:
            canonical_vps+=self.apply(relcl, override_deps={'nsubj':canonicalized_np})
        for attr in attrs:
            canonical_vps+=[]

        return (canonicalized_np,canonical_vps)
    
    def apply(self, vp_node:Node, subject=None,override_deps:Dict=None, *args, **kwargs):
        children=vp_node.get_children()
        child_deps=children.dep

        if subject is not None and not ("nsubj" in child_deps or "nsubjpass" in child_deps):
            '''replace or add given subject to the given vp'''
            children.append(subject)

        if override_deps is not None and len(override_deps.keys())>0:
            for override_dep_key, override_dep_value in override_deps.items():
                override_children=[]
                for child in children:
                    if child.dep==override_dep_key:
                        override_children.append(override_dep_value)
                    else:
                        override_children.append(child)
                children=override_children

        exploded_children=[]
        canonical_nodes=[]

        subject=vp_node.find_out_nodes(type="constituent",dep__in=["nsubj","nsubjpass"]).first()

        if vp_node.is_coordination:
            vp_list_elements=self.get_list_elements(vp_node)
            for vp_list_element in vp_list_elements:
                canonical_nodes+=self.apply(vp_list_element,subject=subject)
        else:
            for child in children:
                if child.constituent_type=="np":
                    if child.is_coordination:
                        list_elements=self.get_list_elements(child)
                        canonicalized_list_elements=[]
                        for list_element in list_elements:
                            canonicalized_list_element, canonicalized_child_vps=self.get_canonicalized_vps_from_np(list_element)
                            canonicalized_list_elements.append(canonicalized_list_element)
                            canonical_nodes+=canonicalized_child_vps
                        exploded_children.append(canonicalized_list_elements)
                    else:
                        np,vps=self.get_canonicalized_vps_from_np(child)
                        exploded_children.append([np])
                        canonical_nodes+=vps
                elif child.constituent_type=="advcl":
                    self.apply(child)
                elif child.is_coordination:
                        exploded_children.append(self.get_list_elements(child))
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