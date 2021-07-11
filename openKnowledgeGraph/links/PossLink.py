from openKnowledgeGraph.links.Link import Link


class PossLink(Link):

    def __init___(self, source_id, target_id):
        Link.__init__(self, source_id, target_id)

    @staticmethod
    def get_type():
        return "poss"
