from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.queries.QuerySet import Q


class TokenNode(Node):

    def __init__(self, text=None, i=None, pos=None, lemma=None, dep=None, tag=None):
        Node.__init__(self)
        self.text = text
        self.i = i
        self.pos = pos
        self.lemma = lemma
        self.dep = dep
        self.tag = tag

    @property
    def full_text(self):
        all_deps = self.traverse_by_out_links(query=Q(type="dependency")).order_by(
            lambda node: node.i)
        full_text = [dep.text for dep in all_deps]
        return ' '.join(full_text)

    @staticmethod
    def get_type():
        return "token"

    def is_passive(self):
        return self.dep in ["nsubjpass", "csubjpass"]  # https://universaldependencies.org/u/dep/

    def is_active(self):
        return self.dep in ["nsubj", "dobj", "pobj"]

    @property
    def voice(self):
        if self.is_passive():
            return "passive"
        elif self.is_active():
            return "active"
        else:
            return None

    def is_past_tense(self):
        self._check_if_tag_exists()
        return self.tag in ["vbd", "vbn"]

    def is_present_tense(self):
        self._check_if_tag_exists()
        return self.tag in ["vgb", "vbp", "vbz"]

    @property
    def tense(self):
        if self.is_past_tense():
            return "past"
        elif self.is_present_tense():
            return "present"
        else:
            return None  # does not apply (e.g. for subject,object, etc.)

    def is_plural(self):
        self._check_if_tag_exists()
        return self.tag in ["nns", "nnps"] or self.tag == "prp" and self.text.lower() in ["they", "their", "them", "we",
                                                                                          "he"]

    @property
    def negated(self):
        if self._is_verb():
            return self.is_negated()
        else:
            return None

    def is_negated(self):
        return bool(self.find_out_links(Q(type="dependency", attr__dependency_type="neg")).first())

    @property
    def preview(self):
        return self.text

    def _is_verb(self):
        return self.pos in ["verb", "aux", "auxpass"]

    @property
    def number(self):
        if self.is_singular():
            return "singular"
        elif self.is_plural():
            return "plural"
        else:
            return None

    def _check_if_tag_exists(self):
        if not self.tag:
            raise Exception(
                "cannot asses tense, or singular/plural without tag information. Did you forget to add the tagger to the spacy pipeline?")

    def is_singular(self):
        self._check_if_tag_exists()
        return self.tag in ["nn", "nnp"] or self.tag == "prp" and self.text.lower() in ["him", "his", "i", "you", "he",
                                                                                        "she", "it"]

    @staticmethod
    def from_spacy_token(graph, token):
        token_node = graph.create_node(node_type="token", properties={"text": token.text,
                                                                      "lemma": token.lemma_,
                                                                      "i": token.i,
                                                                      "pos": token.pos_.lower(),
                                                                      "tag": token.tag_.lower(),
                                                                      "dep": token.dep_.lower()})

        return token_node
