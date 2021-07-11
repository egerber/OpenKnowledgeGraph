from openKnowledgeGraph.selections.GroupedEntities import GroupedEntities


class GroupedLinks(GroupedEntities):

    def __init__(self, graph, nodes_by_group):
        GroupedEntities.__init__(self, graph, nodes_by_group)

    @staticmethod
    def get_type():
        return "GroupedLinks"

    def top(self, k=10):
        return GroupedLinks(self.graph, self.get_top_entities(k))
