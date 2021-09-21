from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry


class ArgumentLink(Link):

    def __init__(self, source_id, target_id, argument_type=None,**kwargs):
        Link.__init__(self, source_id, target_id, attributes={"argument_type": argument_type},**kwargs)

    @staticmethod
    def get_type():
        return "argument"
