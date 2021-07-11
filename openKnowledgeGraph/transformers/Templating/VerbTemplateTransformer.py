from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.TextPart import TextPart
from openKnowledgeGraph.transformers.NodeTransformer import NodeTransformer


class VerbTemplateTransformer(NodeTransformer):

    def __init__(self, **kwargs):
        NodeTransformer.__init__(self, **kwargs)

    def get_pattern(self):
        return Q(type="vp")

    def apply(self, node, *args, **kwargs):
        verb_parts = node.reference.traverse_by_out_links(
            query=Q(type="dependency", attr__dependency_type__in=["auxpass", "aux", "neg"])).order_by(lambda t: t.i)

        verb_text = ' '.join([verb_part.text for verb_part in verb_parts])

        direct_modifiers = '' #advmods that directly precede the verb (as apposed to those that lie behind arguments)

        return TextPart(value=verb_text)
