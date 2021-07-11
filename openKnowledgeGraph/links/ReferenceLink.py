from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class ReferenceLink(Link):

    def __init__(self, source_id, target_id, attributes={}):
        Link.__init__(self,
                      source_id=source_id,
                      target_id=target_id,
                      attributes=attributes)

    @staticmethod
    def get_type():
        return "reference"


