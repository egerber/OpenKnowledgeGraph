from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart
from openKnowledgeGraph.templates.TextPart import TextPart
from openKnowledgeGraph.templates.Template import Template


class AdjpTemplateTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

        from openKnowledgeGraph.transformers.Templating.PrepTemplateTransformer import \
            PrepTemplateTransformer
        self.prep_template_transformer = PrepTemplateTransformer()

    def apply(self, adjp_node, *args, **kwargs):
        template = Template(value=adjp_node)

        preposition = adjp_node.find_child_by_type(type="pp")

        template.add_part("adjp", ArgumentPart(adjp_node))
        if preposition:
            template.add_part("preposition", self.prep_template_transformer.apply(preposition, *args, **kwargs))

        return template
