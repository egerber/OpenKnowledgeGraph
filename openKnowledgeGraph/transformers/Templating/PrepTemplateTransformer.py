from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart
from openKnowledgeGraph.templates.PPTemplate import PPTemplate
from openKnowledgeGraph.templates.TextPart import TextPart


class PrepTemplateTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

        from openKnowledgeGraph.transformers.Templating.NPTemplateTransformer import \
            NPTemplateTransformer

        self.np_template_transformer = NPTemplateTransformer()

    def get_pattern(self):
        return Q(type="pp")

    def apply(self, pp_node, *args, **kwargs):
        chained_preposition = pp_node.get_preposition()  # e.g. Acccording TO ...
        prepositional_object = pp_node.get_object()

        template = PPTemplate(value=pp_node)
        if prepositional_object:
            template.add_part("preposition", TextPart(value=pp_node.text))
            template.add_part("object", self.np_template_transformer.apply(prepositional_object))
        elif chained_preposition:
            chained_text = pp_node.text + ' ' + chained_preposition.text
            template.add_part("preposition", TextPart(value=chained_text))
            chained_prepositional_object = chained_preposition.get_object()
            if chained_prepositional_object:
                template.add_part("object", self.np_template_transformer.apply(chained_prepositional_object))
        return template
