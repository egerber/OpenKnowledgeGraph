from openKnowledgeGraph.links.Link import Link


class PossLink(Link):

    def __init___(self, source_id, target_id,**kwargs):
        Link.__init__(self, source_id, target_id,**kwargs)

    @staticmethod
    def get_type():
        return "poss"
