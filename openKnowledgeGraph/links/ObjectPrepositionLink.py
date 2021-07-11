from openKnowledgeGraph.links.Link import Link


class ObjectPrepositionLink(Link):

    def __init__(self, source_id, target_id):
        Link.__init__(self, source_id, target_id)

    @staticmethod
    def get_type():
        return "object_preposition"
