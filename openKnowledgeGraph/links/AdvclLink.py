from openKnowledgeGraph.links.Link import Link


class AdvclLink(Link):

    def __init__(self, source_id, target_id, adverbial_clause_type=None):
        Link.__init__(self, source_id, target_id, {"type": adverbial_clause_type})

    @staticmethod
    def get_type():
        return "adverbialClause"
