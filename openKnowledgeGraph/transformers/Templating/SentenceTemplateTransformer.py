from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.Templates import Templates
from openKnowledgeGraph.templates.TextPart import TextPart
from openKnowledgeGraph.templates.Template import Template
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


def dep_to_argument_type(dep):
    if dep.startswith("nsubj"):
        return "subject"
    elif dep.endswith("obj"):
        return "object"
    else:
        return "undefined"


class SentenceTemplateTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

        from openKnowledgeGraph.transformers.Templating.AdjpTemplateTransformer import \
            AdjpTemplateTransformer
        from openKnowledgeGraph.transformers.Templating.AdvclTemplateTransformer import \
            AdvclTemplateTransformer
        from openKnowledgeGraph.transformers.Templating.AdvpTemplateTransformer import \
            AdvpTemplateTransformer
        from openKnowledgeGraph.transformers.Templating.NPTemplateTransformer import \
            NPTemplateTransformer
        from openKnowledgeGraph.transformers.Templating.PrepTemplateTransformer import \
            PrepTemplateTransformer
        from openKnowledgeGraph.transformers.Templating.VerbTemplateTransformer import \
            VerbTemplateTransformer

        self.prep_template_transformer = PrepTemplateTransformer()
        self.np_template_transformer = NPTemplateTransformer()
        self.advcl_template_transformer = AdvclTemplateTransformer()

        from openKnowledgeGraph.transformers.Templating.SbarTemplateTransformer import \
            SbarTemplateTransformer
        self.sbar_template_transformer = SbarTemplateTransformer()
        self.advp_template_transformer = AdvpTemplateTransformer()
        self.verb_template_transformer = VerbTemplateTransformer()
        self.adjp_template_transformer = AdjpTemplateTransformer()

    def get_pattern(self):
        return Q(type="independent_clause")

    def find_candidate_nodes(self, graph):
        candidate_nodes = super().find_candidate_nodes(graph)
        return [candidate_node.reference for candidate_node in candidate_nodes]

    def apply(self, independent_clause_node, *args, **kwargs):
        template = Template(independent_clause_node)

        constituents = independent_clause_node.constituents
        constituents.append(independent_clause_node)  # add self (verb)
        for constituent in sorted(constituents, key=lambda c: c.i):
            if constituent == independent_clause_node:
                template.add_part("verb",
                                  self.verb_template_transformer.apply(
                                      independent_clause_node))  # TODO make VerbTemplate
            else:
                if constituent.type == "pp":
                    if constituent.i < independent_clause_node.i:
                        template.add_part("preposition", self.prep_template_transformer.apply(constituent))
                    else:
                        template.add_part("postposition", self.prep_template_transformer.apply(constituent))
                elif constituent.type == "np":
                    link = constituent.find_in_links(type="constituent").first()
                    argument_type = dep_to_argument_type(link.get_attribute("constituent_type"))
                    template.add_part(argument_type, self.np_template_transformer.apply(constituent))
                elif constituent.type == "advcl":
                    template.add_part("advcl", self.advcl_template_transformer.apply(constituent))
                elif constituent.type == "sbar":
                    template.add_part("sbar", self.sbar_template_transformer.apply(constituent))
                elif constituent.type == "adjp":
                    template.add_part("adjp", self.adjp_template_transformer.apply(constituent))
                elif constituent.type == "advp":
                    if constituent.i < independent_clause_node.i:
                        template.add_part("pre_modifier", self.advp_template_transformer.apply(constituent))
                    else:
                        template.add_part("post_modifier", self.advp_template_transformer.apply(constituent))
        return template

    def __call__(self, *args, **kwargs):
        elements = super().__call__(*args, **kwargs)

        return Templates(elements)
