from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.constituents.ConstituentNode import ConstituentNode
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.templates.ArgumentPart import ArgumentPart


class NPNode(ConstituentNode):

    def __init__(self, **kwargs):
        ConstituentNode.__init__(self, **kwargs)
        if 'voice' in kwargs:
            self._voice = kwargs['voice']

    @property
    def is_corefed(self):
        return len(self._get_links_list(type="coref")) > 0

    @property
    def corefed(self):
        return self.get_corefed(recursive=False)

    @property
    def deep_corefed(self):
        return self.get_corefed(recursive=True)

    def get_corefed(self, recursive=False):
        """
        :param recursive: resolves coreferences recursively
        :return:
        """
        coref_links = self._get_links_list(type="coref")
        if len(coref_links) > 0:
            corefed_node = coref_links[0].target
            if recursive:
                return corefed_node.get_corefed(recursive)
            else:
                return corefed_node
        else:
            return self

    def get_preposition(self):
        preposition_links = self._get_out_links_list(type="argument", attr__argument_type="preposition")
        if len(preposition_links) > 0:
            return preposition_links[0].target

    def get_prepositional_object(self):
        preposition = self.get_preposition()
        if preposition:
            return preposition.get_object()
        return None

    def get_word_frequency(self):
        pass

    def get_word_embedding(self):
        pass

    def is_compound(self):
        pass

    def get_compounds(self):
        compound_elements = self.reference.find_out_nodes(type="token", dep="compound")
        compound_elements.append(self)
        return list(sorted(compound_elements, key=lambda c: c.i))

    @property
    def compound_text(self):
        compounds = self.get_compounds()
        return ' '.join([c.text for c in compounds])

    @staticmethod
    def get_type():
        return "np"

    @property
    def is_list(self):
        return self.find_out_links(Q(type="list_element"))

    def get_list_elements(self):
        '''
        returns conj elements from dependency tree (e.g. Paul, Lisa, and Marie -> [(Paul, Lisa and Marie), (Paul), (Lisa), (Marie)]
        :return:
        '''
        list_elements = [self]
        for list_element in self.find_out_links(Q(type="list_element")).target_nodes.filter(type="np"):
            list_elements += list_element.get_list_elements()

        return list_elements

    @property
    def voice(self):
        if self._voice:
            return self._voice
        else:
            return self.reference.voice

    @property
    def number(self):
        if self.is_list:
            return "plural"
        else:
            return self.reference.number

    @staticmethod
    def from_token_node(token_node):
        graph = token_node.get_graph()
        np_node = NPNode(reference_node=token_node, voice=token_node.voice)
        graph.add_node(np_node)

        ConstituentNode.add_reference_link(np_node, token_node)
        ConstituentNode.link_constituents(np_node, token_node)

        return np_node

    def get_type_string(self):
        type_string = "np"
        if self.ner is not None:
            type_string += ":{}".format(self.ner)

        return type_string
