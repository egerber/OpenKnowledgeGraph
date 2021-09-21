from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.templates.AdvclTemplate import AdvclTemplate
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart
from openKnowledgeGraph.templates.TextPart import TextPart
from openKnowledgeGraph.templates.Template import Template


class AdvpTemplateTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def apply(self, advp_node, *args, **kwargs):
        template = Template(value=advp_node)

        template.add_part("advp", ArgumentPart(advp_node, *args, **kwargs))
        return template
