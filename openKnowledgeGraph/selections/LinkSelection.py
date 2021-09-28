from __future__ import annotations
from collections import defaultdict

from openKnowledgeGraph.queries.QueryHelper import filter_entities
from openKnowledgeGraph.selections.EntitySelection import EntitySelection
from openKnowledgeGraph.selections.GroupedLinks import GroupedLinks
from openKnowledgeGraph.utils.listutils import unique_items


class LinkSelection(EntitySelection):

    def __init__(self, graph, selected_links=None):
        EntitySelection.__init__(self, graph, selected_links)

    def create_selection(self, items):
        return LinkSelection(self.graph, items)

    @property
    def nodes(self):
        return self.get_nodes()

    @property
    def source_nodes(self):
        return self.get_source_nodes()

    @property
    def target_nodes(self):
        return self.get_target_nodes()

    def create_grouped_selection(self, groups):
        return GroupedLinks(self.graph, groups)

    def _get_nodes_list(self):
        nodes = []
        for link in self:
            nodes.append(link.source)
            nodes.append(link.target)

        return unique_items(nodes)

    def _get_target_nodes_list(self):
        target_nodes = []
        for link in self:
            target_nodes.append(link.target)

        return unique_items(target_nodes)  # could be implemented more efficiently in the future

    def _get_source_nodes_list(self):
        source_nodes = []
        for link in self:
            source_nodes.append(link.source)

        return unique_items(source_nodes)  # could be implemented more efficiently in the future

    def get_target_nodes(self):
        from openKnowledgeGraph.selections.NodeSelection import NodeSelection
        return NodeSelection(self.graph, self._get_target_nodes_list())

    def get_source_nodes(self):
        from openKnowledgeGraph.selections.NodeSelection import NodeSelection
        return NodeSelection(self.graph, self._get_source_nodes_list())

    def get_nodes(self):
        from openKnowledgeGraph.selections.NodeSelection import NodeSelection

        return NodeSelection(self.graph, self._get_nodes_list())

    def find_source_nodes(self, query=None, **query_args):
        return self.source_nodes.filter(query=query, **query_args)

    def find_target_nodes(self, query=None, **query_args):
        return self.target_nodes.filter(query=query, **query_args)

    def filter(self, query=None, **query_args):
        return LinkSelection(self.graph, filter_entities(self.selected_entities, query=query, **query_args))

    def intersect(self, other_selection: LinkSelection) -> LinkSelection:
        return super().intersect(other_selection)


    def order_by(self, sort_func=lambda node: node.get_id()):
        return LinkSelection(self.graph, sorted(self.selected_entities, key=sort_func))

    def __repr__(self):
        return "<Link Selection with {} links>".format(len(self.selected_entities)) + self._preview_items()
