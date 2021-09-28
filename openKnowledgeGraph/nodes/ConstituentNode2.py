from __future__ import annotations
from openKnowledgeGraph.selections.NodeSelection import NodeSelection
from typing import List
import logging

from openKnowledgeGraph.nodes import TokenNode
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.nodes.NoneNode import NoneNode
from openKnowledgeGraph.queries.QuerySet import Q



class ConstituentNode2(Node):

    name="constituent"
    computed_properties=["full_text","is_coordination"]

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @property
    def children(self) -> NodeSelection:
        return self.get_children()

    def get_children(self) -> NodeSelection:
        return self.find_out_links(type="constituent").target_nodes

    @property
    def is_coordination(self):
        for child in self.children:
            if child.dep=="conj":
                return True

        return False

    @property
    def full_text(self):
        nested_children = self.traverse_by_out_links(query=Q(type="constituent")).order_by(
            lambda node: node.i)
        
        full_text = [f'{child.text}{child.whitespace}' for child in nested_children]

        return ''.join(full_text)