from openKnowledgeGraph.selections.LinkSelection import LinkSelection
from openKnowledgeGraph.selections.NodeSelection import NodeSelection
from typing import List


class GraphSelection:
    """
    represents a subset of links and nodes from another graph
    """

    def __init__(self, graph, selected_node_ids:List[str],selected_link_ids:List[str]):
        self.graph = graph
        self.selected_node_ids=selected_node_ids
        self.selected_link_ids=selected_link_ids

    @property
    def nodes(self) -> NodeSelection:
        pass

    @property
    def links(self) -> LinkSelection:
        pass

    def get_original(self):
        return self.graph

    def include_adjacent_nodes(self,depth=1):
        pass

    def __repr__(self):
        return "<KnowledgeGraphSubset with {} nodes and {} links>".format(len(self.link_dictionary),
                                                                          len(self.nodes_by_id))
