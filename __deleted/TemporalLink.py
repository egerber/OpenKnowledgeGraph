from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class TemporalLink(Link):

    def __init__(self, source_id, target_id, attributes={},**kwargs):
        Link.__init__(self,
                      source_id=source_id,
                      target_id=target_id,
                      attributes=attributes,
                      **kwargs)

    @staticmethod
    def get_type():
        return "temporal"
