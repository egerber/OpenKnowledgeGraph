from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class CorefLink(Link):

    def __init__(self, source_id, target_id):
        Link.__init__(self, source_id, target_id)

    @staticmethod
    def get_type():
        return "coref"


