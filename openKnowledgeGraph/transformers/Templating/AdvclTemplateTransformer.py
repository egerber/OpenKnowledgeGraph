from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.templates.AdvclTemplate import AdvclTemplate
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart
from openKnowledgeGraph.templates.TextPart import TextPart


class AdvclTemplateTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    def apply(self, advcl_node,*args,**kwargs):
        mark = advcl_node.get_mark()

        advcl_template = AdvclTemplate(value=advcl_node)
        if mark:
            advcl_template.add_part("mark", TextPart(mark.text))
        advcl_template.add_part("advcl", ArgumentPart(advcl_node))
        return advcl_template
