from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart
from openKnowledgeGraph.templates.NPArgument import NPArgument
from openKnowledgeGraph.templates.TextPart import TextPart
from openKnowledgeGraph.templates.Template import Template


class SbarTemplateTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="sbar")

    def apply(self, node, *args, **kwargs):
        from openKnowledgeGraph.transformers.Templating.SentenceTemplateTransformer import \
            SentenceTemplateTransformer
        self.verb_prep_template_transformer = SentenceTemplateTransformer()
        mark = node.get_mark()
        if mark:
            text = mark.text
        else:
            text = "<mark>"
        template = Template(value=node)
        template.add_part("mark", TextPart(value=text))
        template.add_part("sbar", self.verb_prep_template_transformer.apply(node))

        return template
