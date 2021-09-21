from openKnowledgeGraph.links.Link import Link


class PrepositionLink(Link):

    def __init__(self, source_id, target_id, prep=None,**kwargs):
        Link.__init__(self, source_id, target_id,**kwargs)

        self.prep = prep

    @staticmethod
    def get_type():
        return "preposition"
