import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.TransformerGroup.CanonicalizationTransformer import CanonicalizationTransformer


class TestCanonicalVP(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test1(self):
        text = 'Steve Jobs and Steve Wozniac founded Apple and became successful and rich'
        graph = OpenKnowledgeGraph.from_text(text)

        c_tranf = CanonicalizationTransformer()
        c_tranf(graph)
        
        result_sentences=["Steve Jobs founded Apple",\
            "Steve Jobs became successful",
            "Steve Jobs became rich",
            "Paul Wozniac founded Apple",
            "Paul Wozniac became successful",
            "Paul Wozniac became rich"]

        print(graph.find_nodes(type="canonical_vp"))



if __name__=='__main__':
    unittest.main()