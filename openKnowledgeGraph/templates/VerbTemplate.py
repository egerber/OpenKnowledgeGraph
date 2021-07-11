from openKnowledgeGraph.templates.Template import Template


class VerbTemplate(Template):

    def __init__(self, value):
        super().__init__(value)

        # is value=node?
