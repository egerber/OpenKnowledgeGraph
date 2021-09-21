import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.queries.QuerySet import Q


class TestCoordinations(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def test_vps(self):
        graph = OpenKnowledgeGraph.from_text("Paul was a programmer and Tom is a clerk")

        vps_coordination_given=[vp.full_text for vp in graph.fn(type="vp",is_coordination=True)]
        vps_unit_given=[vp.full_text for vp in graph.fn(type="vp",is_coordination=False)]

        self.assertEqual(vps_coordination_given,["Paul was a programmer and Tom is a clerk"])
        self.assertEqual(vps_unit_given,["Paul was a programmer", "Tom is a clerk"])
    
    def test_nps(self):
        graph = OpenKnowledgeGraph.from_text("Paul, Tim, and Jim are singers",model='en_core_web_sm')
        
        subject=graph.fn(type="np",is_coordination=True).first()

        coordinations=subject.get_coordinates()
        self.assertEqual(len(coordinations),3)
        self.assertEqual(graph.fn(type="np",is_coordination=False).count(),4)