from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.ConstituentTransformer2 import ConstituentTransformer2
import unittest


class TestConstituents2(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_properties(self):
        text = 'Apples and tomatoes are red'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm',components=['token','dependency'])

        constituent_transformer2=ConstituentTransformer2()
        constituent_transformer2(graph)

        root_vp=graph.fn(type="constituent2",dep="root")[0]
        self.assertEqual(root_vp.full_text, text)
        self.assertEqual(root_vp.text,"are")
        self.assertEqual(root_vp.constituent_type,"vp")

    def test_coordinations(self):
        text='apples and tomatoes are red, and oranges are orange and juicy'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm',components=['token','dependency'])

        constituent_transformer2=ConstituentTransformer2()
        constituent_transformer2(graph)

        self.assertEqual(graph.fn(type="constituent2",constituent_type="np",is_coordination=True).full_text,["apples and tomatoes "])
        self.assertEqual(graph.fn(type="constituent2",constituent_type="vp",is_coordination=True).full_text,[text])
        self.assertEqual(graph.fn(type="constituent2",constituent_type="advp",is_coordination=True).full_text,["orange and juicy"])
        


