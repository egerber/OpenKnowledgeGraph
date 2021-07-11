from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart
from openKnowledgeGraph.templates.NPArgument import NPArgument
from openKnowledgeGraph.templates.Template import Template
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer
from openKnowledgeGraph.transformers.Templating.NounTemplateTransformer import \
    NounTemplateTransformer


class NPTemplateTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)
        self._prep_template_transformer = None
        self.noun_template_transformer = NounTemplateTransformer()

    @property
    def prep_template_transformer(self):
        if self._prep_template_transformer is None:
            from openKnowledgeGraph.transformers.Templating.PrepTemplateTransformer import \
                PrepTemplateTransformer
            self._prep_template_transformer = PrepTemplateTransformer()
        return self._prep_template_transformer

    def get_pattern(self):
        return Q(type="np")

    def apply(self, node, *args, **kwargs):
        '''should cover the following cases
        - relative clause
        - prepositional case
        - adjectives
        - numeral
        - date
        '''

        template = Template(node)
        constituents = node.constituents
        constituents.append(node)  # add self (verb)
        for constituent in sorted(constituents, key=lambda c: c.i):
            if constituent == node:
                template.add_part("np", self.noun_template_transformer.apply(node))
            elif constituent.type == "pp":
                template.add_part("postposition", self.prep_template_transformer.apply(constituent))
            else:
                pass
                # print("np_template no type for ", constituent.type)
        return template
