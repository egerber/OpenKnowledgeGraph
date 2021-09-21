from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.NPArgument import NPArgument
from openKnowledgeGraph.templates.Template import Template
from openKnowledgeGraph.templates.TextPart import TextPart


class NounTemplateTransformer(GraphOperation):

    def __init__(self):
        GraphOperation.__init__(self)

    def get_pattern(self):
        return Q(type="np")

    def apply(self, node, *args, **kwargs):
        noun_parts = node.reference.find_out_links(
            query=Q(type="dependency", dependency_type__in=["amod", "nummod"])).order_by(lambda t: t.i)

        nounTemplate = Template(node)
        if len(noun_parts) > 0:
            noun_modifiers = ' '.join([noun_part.text for noun_part in noun_parts])
            nounTemplate.add_part("noun_modifier", TextPart(noun_modifiers))
        nounTemplate.add_part("np", NPArgument(node))

        return nounTemplate
