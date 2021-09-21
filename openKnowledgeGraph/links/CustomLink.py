from openKnowledgeGraph.links.Link import Link


class CustomLink(Link):
    def __init__(self, link_type, **kwargs):
        Link.__init__(self, **kwargs)
        self.link_type = link_type

    def get_type(self):
        return self.link_type
