from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.queries.QuerySet import Q
import re

from openKnowledgeGraph.templates.TextPart import TextPart


class VPNode(ConstituentNode):

    name="vp"
    
    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)

    def get_adjectives(self):
        pass

    def get_subject(self):
        return self.find_child_by_type("subject")

    def get_object(self):
        return self.find_child_by_type("object")

    def get_aux_elements(self):
        aux_elements = self.reference.find_out_nodes(type="token", dep__in=["aux", "auxpass"])
        aux_elements.append(self)
        return list(sorted(aux_elements, key=lambda c: c.i))

    @property
    def aux_text(self):
        '''
        returns root verb combined with AUX modifiers
        :return:
        '''
        aux_elements = self.get_aux_elements()
        return ' '.join([c.text for c in aux_elements])

    def get_prepositional_object(self):
        preposition = self.get_preposition()
        if preposition:
            return preposition.find_out_nodes(type="token", dep="pobj").first()
        else:
            return None

    def get_preposition(self):
        return self.reference.find_out_nodes(type="token", dep="prep").first()

    def get_pre_preposition(self):
        self.reference.find_out_nodes(type="token", dep="prep", custom=lambda prep: prep.i < self.i).first()

    def get_post_preposition(self):
        self.reference.find_out_nodes(type="token", dep="prep", custom=lambda prep: prep.i > self.i).first()

    @staticmethod
    def from_token_node(token_node, override_deps=None):
        graph = token_node.graph

        vp_node = graph.create_node(node_type="vp")
        graph.add_node(vp_node)

        ConstituentNode.add_reference_link(vp_node, token_node)
        ConstituentNode.link_constituents(constituent_node=vp_node,
                                          token_node=token_node,
                                          override_deps=override_deps)

        return vp_node
