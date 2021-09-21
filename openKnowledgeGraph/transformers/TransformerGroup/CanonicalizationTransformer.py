import itertools

from openKnowledgeGraph.nodes import CanonicalVPNode
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q


class CanonicalizationTransformer(GraphOperation):

    def __init__(self, canonicalize_properties=None, resolve_corefs=True, resolve_relcls=True, **kwargs):
        GraphOperation.__init__(self, **kwargs)
        if canonicalize_properties is None:
            canonicalize_properties = ['nsubj', 'nsubjpass', 'dobj', 'attr', 'acomp', 'advmod', 'amod']
        self.canonicalize_properties = canonicalize_properties
        self.resolve_corefs = resolve_corefs
        self.resolve_relcls = resolve_relcls

    def get_pattern(self):
        return Q(type="vp", is_list_element__not=True)

    @staticmethod
    def create_canonicalized_clause(original_vp, children):
        graph = original_vp.graph
        canonical_phrase = graph.create_reference_node(node_type="canonical_vp", reference_node=original_vp)
        for child in children:
            graph.create_link("constituent", source=canonical_phrase, target=child, constituent_type=child.dep)

        return canonical_phrase

    def apply_vp_coordination(self, vp_coordination, root=None):
        canonical_phrases = []

        combinatorical_children = []

        has_subject = False

        if self.resolve_relcls and vp_coordination.dep == "relcl":
            pass  # TODO inherit subject from parent

        for child in vp_coordination.children:
            if child.dep=="relcl":
                root=vp_coordination.find_in_links(type="constituent").first().source
                constituent=child.find_in_links(type="constituent").first().source
                self.apply_vp_coordination(constituent, root)

            if self.resolve_corefs and child.type == "np" and child.is_corefed:
                child = child.corefed

            if child.dep in self.canonicalize_properties and child.is_coordination:
                combinatorical_children.append(child.get_coordinates())
            else:
                combinatorical_children.append([child])
            if child.dep in ["nsubj", "nsubjpass"]:
                has_subject = True

        if not has_subject and root is not None:  # try to inherit subject from parent
            parent_subject = root.find_children(type="np",dep__in=["nsubj", "nsubjpass"]).first()
            if parent_subject:
                combinatorical_children.append(parent_subject.get_coordinates())

        for canonical_children in itertools.product(*combinatorical_children):
            canonical_phrases.append(
                self.create_canonicalized_clause(original_vp=vp_coordination, children=canonical_children))

        return canonical_phrases

    def apply(self, vp_node, *args, **kwargs):
        canonical_phrases = []
        if vp_node.is_coordination:
            vp_coordinations = vp_node.get_coordinates()

            for vp_coordination in vp_coordinations:
                canonical_phrases += self.apply_vp_coordination(vp_coordination, root=vp_coordinations[0])
        else:
            canonical_phrases += self.apply_vp_coordination(vp_node, root=None)
        return canonical_phrases

    @staticmethod
    def get_dependencies():
        return ["dependency"]

    @staticmethod
    def get_name():
        return "canonical"