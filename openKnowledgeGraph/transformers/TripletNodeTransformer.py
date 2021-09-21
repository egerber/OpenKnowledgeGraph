from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
import os

from openKnowledgeGraph.queries.QuerySet import Q
import itertools

from statements.TripletNode import TripletNode

DEBUG = os.environ.get('DEBUG', False)


class TripletNodeTransformer(GraphOperation):

    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)

    @staticmethod
    def get_name():
        return "TripletNodeTransformer"

    @staticmethod
    def get_pattern():
        return Q(type__in=["vp", "advcl"], custom=lambda vp: vp.get_subject() or vp.get_object())

    @staticmethod
    def apply(vp_node):
        subject_np = vp_node.get_subject()
        object_np = vp_node.get_object()

        if subject_np:
            np_subject_list_elements = subject_np.get_list_elements()
        else:
            np_subject_list_elements = [None]

        if object_np:
            np_object_list_elements = object_np.get_list_elements()
        else:
            np_object_list_elements = [None]

        # add triplet for all list elements in subject (Paul and Lisa) and object (coffee and cake) -> (Paul, eat, cake), (Lisa, eat, cake)
        for combination in itertools.product(np_subject_list_elements, np_object_list_elements):
            TripletNode.from_subject_predicate_object(combination[0], vp_node, combination[1])
