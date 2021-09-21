from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class DependencyLink(Link):

    def __init__(self, source_id, target_id, dependency_type=None,**kwargs):
        Link.__init__(self, source_id, target_id, attributes={'dependency_type': dependency_type},**kwargs)

    @staticmethod
    def get_type():
        return "dependency"
