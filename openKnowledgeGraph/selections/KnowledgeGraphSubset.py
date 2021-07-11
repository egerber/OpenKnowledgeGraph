class KnowledgeGraphSubset:
    """
    decorates an original knowledge graph
    """

    def __init__(self, graph, nodes_by_id, link_dictionary):
        self.graph = graph
        self.link_dictionary = link_dictionary
        self.nodes_by_id = nodes_by_id

    def get_original(self):
        return self.graph

    def include_adjacent_nodes(self,depth=1):
        pass

    def __repr__(self):
        return "<KnowledgeGraphSubset with {} nodes and {} links>".format(len(self.link_dictionary),
                                                                          len(self.nodes_by_id))
