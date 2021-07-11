from openKnowledgeGraph.links.Link import Link


class AdvmodLink(Link):

    def __init__(self, source_id, target_id, advmod=None):
        Link.__init__(self, source_id, target_id)

        self.advmod = advmod

    @staticmethod
    def get_type():
        return "advmod"
