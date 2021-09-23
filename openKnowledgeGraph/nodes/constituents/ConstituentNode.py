from __future__ import annotations
from typing import List
import logging

from openKnowledgeGraph.nodes import TokenNode
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.nodes.NoneNode import NoneNode
from openKnowledgeGraph.queries.QuerySet import Q


def filter_none(arr):
    return [el for el in arr if el is not None]


class ConstituentNode(Node):

    type="constituent"
    computed_properties=["is_coordination"]

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @property
    def root(self):
        return self.get_reference_node()

    @property
    def constituents(self):
        return self.get_constituents()

    def get_constituents(self):
        return self.get_arguments()

    def get_left_children(self):
        return [child for child in self.get_children() if child.i < self.i]

    def get_right_children(self):
        return [child for child in self.get_children() if child.i > self.i]

    def get_children(self):
        children = self.find_out_links(type="constituent").target_nodes
        return list(sorted(children, key=lambda child: child.i))

    @property
    def left_children(self):
        return self.get_left_children()

    @property
    def preview(self):
        return self.text

    @property
    def right_children(self):
        return self.get_right_children()

    @property
    def children(self):
        return self.get_children()

    def get_arguments(self):
        return self.find_out_links(type="constituent").target_nodes

    def find_children(self, *queries, **query_args):
        return self.find_out_links(type="constituent").target_nodes.filter(*queries, **query_args)

    def find_child_by_type(self, type):
        arguments = self.find_out_links(type="constituent", constituent_type=type).target_nodes
        if len(arguments) > 0:
            return arguments.first()
        else:
            return NoneNode.create_for_node(self)

    @property
    def full_text(self):
        nested_children = self.traverse_by_out_links(query=Q(type__in=["list","constituent"])).filter(type="token").order_by(
            lambda node: node.i)
        full_text = [child.text for child in nested_children]
        return ' '.join(full_text)

    @staticmethod
    def add_reference_link(constituent_node, token_node):
        graph = token_node.graph

        graph.create_link("reference", constituent_node, token_node)

    @staticmethod
    def link_constituents(constituent_node, token_node, override_deps=None):
        if override_deps is None:
            override_deps = {}

        _registered_overriden_dependencies = []
        for dep_node in token_node.find_out_nodes(type="token"):
            dep = dep_node.dep

            if dep in ["nsubj", "nsubjpass"] and "nsubj" in override_deps or "nsubjpass" in override_deps:
                '''
                special case because nsubjpass can override nsubj and vice versa
                '''
                if "nsubj" in override_deps:
                    dep_node = override_deps["nsubj"]
                    _registered_overriden_dependencies.append("nsubj")
                elif "nsubjpass" in override_deps:
                    dep_node = override_deps["nsubjpass"]
                    _registered_overriden_dependencies.append("nsubjpass")
            elif dep in override_deps:
                dep_node = override_deps[dep]
                _registered_overriden_dependencies.append(dep)

            if dep_node is None:
                '''was overriden to be not defined'''
                continue
            ConstituentNode.link_constituent(constituent_node, dep_node)

        '''
        incase that dependency is not overriden, but extended iterate over overide_deps again
        '''
        for dep, override_node in override_deps.items():
            if dep not in _registered_overriden_dependencies and override_node is not None:
                ConstituentNode.link_constituent(constituent_node, override_node)

        token_node.graph.create_link(
            "constituent", 
            source=constituent_node, 
            target=token_node, 
            constituent_type="leaf")

        

    @property
    def is_coordination(self) -> bool:
        '''returns whether the phrase is a conjunctive/disjunctive coordination (X and Y, X or Y, ...)'''
        return self.find_out_links(type="list").count()>0

    def get_coordinates(self) -> List[ConstituentNode]:
        if self.is_coordination:
            return self.find_out_links(type="list").target_nodes
        else:
            return [self]

    @staticmethod
    def link_constituent(constituent_node: ConstituentNode, token_node: TokenNode):
        graph = token_node.graph
        CONSTITUENTS = ["np", "vp", "sbar", "adjp", "advp", "pp", "advcl"]

        child_constituents = token_node.find_in_nodes(type__in=CONSTITUENTS)
        if len(child_constituents) > 1:
            '''
            if mulitple constituents are associated with given constituent, one of them must be the list root while the 
            other one are list elements (e.g. [X and Y] vs [X] vs [Y])
            '''
            coordination_constituents = child_constituents.filter(is_coordination=True)
            if len(coordination_constituents) != 1:
                logging.error("could not identify root constituent for {}".format(token_node))
            child_constituent = coordination_constituents.first()
        else:
            child_constituent = child_constituents.first()

        if child_constituent:
            graph.create_link("constituent", constituent_node, child_constituent, constituent_type=token_node.dep)
        else:
            graph.create_link("constituent", constituent_node, token_node, constituent_type="leaf")
            # TODO register as leaf
            '''
            dep is no constituent (e.g. det, amod, punct, cc, etc.
            '''
            pass