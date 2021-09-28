from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.ConstituentTransformer import ConstituentTransformer
import unittest


class TestConstituents(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_properties(self):
        text = 'Apples and tomatoes are red'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm',components=['token','dependency','constituent'])

        root_vp=graph.fn(type="constituent",dep="root")[0]
        self.assertEqual(root_vp.full_text, text)
        self.assertEqual(root_vp.text,"are")
        self.assertEqual(root_vp.constituent_type,"vp")

    def test_coordinations(self):
        text='apples and tomatoes are red, and oranges are orange and juicy'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm',components=['token','dependency','constituent'])

        self.assertEqual(graph.fn(type="constituent",constituent_type="np",is_coordination=True).full_text,["apples and tomatoes "])
        self.assertEqual(graph.fn(type="constituent",constituent_type="vp",is_coordination=True).full_text,[text])
        self.assertEqual(graph.fn(type="constituent",constituent_type="advp",is_coordination=True).full_text,["orange and juicy"])
        


