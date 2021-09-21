from __future__ import annotations
from typing import List
import logging

from openKnowledgeGraph.nodes import TokenNode
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.nodes.NoneNode import NoneNode
from openKnowledgeGraph.queries.QuerySet import Q



class ConstituentNode(Node):

    type="constituent2"

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @staticmethod
    def get_computed_properties():
        return ["is_coordination"]

    @property
    def children(self):
        return self.get_children()

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
        nested_children = self.traverse_by_out_links(query=Q(type__in=["constituent"])).filter(type="token").order_by(
            lambda node: node.i)
        full_text = [child.text for child in nested_children]
        return ' '.join(full_text)