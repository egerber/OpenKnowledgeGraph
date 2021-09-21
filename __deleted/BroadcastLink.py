from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class BroadcastLink(Link):

    def __init__(self, source_id, target_id, weight=1.0,**kwargs):
        Link.__init__(self, source_id, target_id,**kwargs)
        self.weight = weight

    @staticmethod
    def get_type():
        return "broadcast"


