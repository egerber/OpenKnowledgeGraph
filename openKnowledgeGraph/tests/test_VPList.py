import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.queries.QuerySet import Q


class TestVPList(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def test_init(self):
        graph = OpenKnowledgeGraph.from_text("Paul Allen was a programmer and Paul McCartney was a singer")

        self.assertEqual(len(graph.find_nodes(Q(type="vp"))), 4)
