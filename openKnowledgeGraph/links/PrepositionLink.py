from openKnowledgeGraph.links.Link import Link


class PrepositionLink(Link):

    def __init__(self, source_id, target_id, prep=None):
        Link.__init__(self, source_id, target_id)

        self.prep = prep

    @staticmethod
    def get_type():
        return "preposition"
