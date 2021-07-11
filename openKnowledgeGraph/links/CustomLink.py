from openKnowledgeGraph.links.Link import Link


class CustomLink(Link):
    def __init__(self, type, **kwargs):
        Link.__init__(self, **kwargs)
        self._type = type

    def get_type(self):
        return self._type
