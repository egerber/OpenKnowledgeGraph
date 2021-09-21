from links.Link import Link
from nodes import NoneNode
from nodes.Node import Node


class TripletNode(Node):

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    def find_argument(self, type):
        outlinks = self._get_out_links_list(type="argument", argument_type=type)
        if len(outlinks) > 0:
            return outlinks[0].target
        else:
            return NoneNode.create_for_node(self)

    def get_subject(self):
        return self.find_argument("subject")

    def get_predicate(self):
        return self.find_argument("predicate")

    def get_object(self):
        return self.find_argument("object")

    @property
    def canonical(self):
        return self.is_canonical()

    @property
    def number(self):
        if self.is_singular():
            return "singular"
        elif self.is_plural():
            return "plural"
        else:
            return None

    @property
    def voice(self):
        if self.is_passive():
            return "passive"
        elif self.is_active():
            return "active"
        else:
            return None

    def is_active(self):
        return self.subject and self.subject.is_active()

    @property
    def negated(self):
        return self.predicate and self.predicate.negated

    def is_canonical(self):
        '''
        returns if both subject and object are single elements (no conjunctions)
        :return:
        '''
        _is_canonical = True
        if self.subject and self.subject.is_list:
            _is_canonical = False
        elif self.object and self.object.is_list:
            _is_canonical = False

        return _is_canonical

    @property
    def tense(self):
        if self.is_past_tense():
            return "past"
        elif self.is_present_tense():
            return "present"
        else:
            return None  # does not apply (e.g. for subject,object, etc.)

    def is_passive(self):
        return self.subject and self.subject.is_passive()

    def is_past_tense(self):
        return self.predicate and self.predicate.is_past_tense()

    def is_present_tense(self):
        return self.predicate and self.predicate.is_present_tense()

    def is_singular(self):
        return self.subject and self.subject.is_singular()

    def is_plural(self):
        return self.subject and self.subject.is_plural()

    @property
    def predicate(self):
        return self.get_predicate()

    @property
    def subject(self):
        return self.get_subject()

    @property
    def object(self):
        return self.get_object()

    @staticmethod
    def get_type():
        return "triplet"

    def get_text(self):
        if self.subject and self.object:
            return "( {} -- {} -- {})".format(self.subject.corefed.full_text, self.predicate.template_string,
                                              self.object.corefed.full_text)
        elif self.subject:
            return "( {} -- {} -- {})".format(self.subject.corefed.full_text, self.predicate.template_string, None)
        elif self.object:
            return "( {} -- {} -- {})".format(None, self.predicate.template_string, self.object.corefed.full_text)

    @staticmethod
    def from_subject_predicate_object(np_subject, vp_predicate, np_object):
        graph = vp_predicate.get_graph()
        triplet = graph.create_node(node_type="triplet")
        graph.add_node(triplet)
        links = []

        if np_subject:
            links.append(
                graph.create_link("argument", triplet, np_subject, argument_type="subject"))
        links.append(graph.create_link("argument", triplet, vp_predicate, argument_type="predicate"))
        if np_object:
            links.append(graph.create_link("argument", triplet, np_object, argument_type="object"))

        graph.add_links(links)

        return triplet

    @staticmethod
    def from_subject_predicate_attr(np_subject, vp_predicate, advp_attr):
        graph = vp_predicate.get_graph()
        triplet = graph.create_node(node_type="triplet")
        graph.add_node(triplet)

        links = []
        if np_subject:
            links.append(
                graph.create_link("argument", triplet, np_subject, argument_type="subject"))
        links.append(graph.create_link("argument", triplet, vp_predicate, argument_type="predicate"))
        if advp_attr:
            links.append(graph.create_link("argument", triplet, advp_attr, argument_type="attribute"))

        graph.add_links(links)
