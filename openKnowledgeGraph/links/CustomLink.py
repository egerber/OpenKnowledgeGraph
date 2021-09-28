from openKnowledgeGraph.links.Link import Link


class CustomLink(Link):
    def __init__(self, **kwargs):
        Link.__init__(self, **kwargs)
