from __future__ import annotations
from openKnowledgeGraph.queries.QueryHelper import filter_entities
from typing import TYPE_CHECKING
from openKnowledgeGraph.selections.EntitySelection import EntitySelection
from openKnowledgeGraph.selections.GroupedNodes import GroupedNodes
from openKnowledgeGraph.selections.LinkSelection import LinkSelection
from openKnowledgeGraph.utils.listutils import unique_items

if TYPE_CHECKING:
    from openKnowledgeGraph.nodes.Node import Node


class NodeSelection(EntitySelection):

    def __init__(self, graph, selected_nodes=None):
        EntitySelection.__init__(self, graph, selected_nodes)

    def create_selection(self, items):
        return NodeSelection(self.graph, items)

    def create_grouped_selection(self, groups):
        return GroupedNodes(self.graph, groups)

    def _get_in_links_list(self):
        in_links = []
        for node in self:
            in_links += node.in_links

        return unique_items(in_links)

    def _get_links_list(self):
        links = []
        for node in self:
            links += node.links

        return unique_items(links)

    def _get_out_links_list(self):
        out_links = []
        for node in self:
            out_links += node.out_links

        return unique_items(out_links)

    @property
    def links(self):
        return LinkSelection(self.graph, self._get_links_list())

    @property
    def in_links(self):
        return LinkSelection(self.graph, self._get_in_links_list())

    def find_in_nodes(self, query=None, **query_args):
        return self.in_nodes.filter(query=query, **query_args)

    def find_out_nodes(self, query=None, **query_args):
        return self.out_nodes.filter(query=query, **query_args)

    def find_adjacent_nodes(self, query=None, **query_args):
        return self.adjacent_nodes.filter(query=query, **query_args)

    def first(self) -> Node:
        return super().first()

    def _get_out_nodes_list(self):
        out_nodes = []
        for link in self.out_links:
            out_nodes.append(link.target)

        return unique_items(out_nodes)

    def _get_in_nodes_list(self):
        in_nodes = []
        for link in self.in_links:
            in_nodes.append(link.source)

        return unique_items(in_nodes)

    def filter(self, query=None, **query_args):
        return NodeSelection(self.graph, filter_entities(self.selected_entities, query=query, **query_args))

    def _get_adjacent_nodes_list(self):
        adjacent_nodes = []
        for link in self.links:
            adjacent_nodes.append(link.source)
            adjacent_nodes.append(link.target)

        return unique_items(adjacent_nodes)

    @property
    def in_nodes(self):
        return NodeSelection(self.get_graph(), self._get_in_nodes_list())

    @property
    def adjacent_nodes(self):
        return NodeSelection(self.get_graph(), self._get_adjacent_nodes_list())

    @property
    def out_nodes(self):
        return NodeSelection(self.get_graph(), self._get_out_nodes_list())

    def clone(self) -> NodeSelection:
        new_nodes=[]
        for node in self:
            cloned_node=self.graph.create_node(node.type, properties=node.get_properties())
            new_nodes.append(cloned_node)
            for out_link in node.find_out_links(type="reference"):
                self.graph.create_link(
                    link_type=out_link.type,
                    source=cloned_node, 
                    target=out_link.target
                )

        return NodeSelection(self.graph, new_nodes)

    @property
    def out_links(self):
        return LinkSelection(self.graph, self._get_out_links_list())

    def find_links(self, query=None, **query_args):
        return self.links.filter(query=query, **query_args)

    def intersect(self, other_selection: NodeSelection) -> NodeSelection:
        return super().intersect(other_selection)

    def __repr__(self):
        return "<Node Selection with {} nodes>".format(len(self.selected_entities)) + self._preview_items()
