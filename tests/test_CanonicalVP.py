import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.TransformerGroup.CanonicalizationTransformer import CanonicalizationTransformer


class TestCanonicalVP(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_coordination1(self):
        text = 'Steve and Paul founded a company and became successful and rich'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        c_tranf = CanonicalizationTransformer()
        c_tranf(graph)
        
        result_sentences=[
            "Steve founded a company",\
            "Paul founded a company",
            "Steve became successful",
            "Paul became successful",
            "Steve became rich",
            "Paul became rich"
        ]

        canonical_vps=graph.fn(type="canonical_vp")
        print([node.full_text for node in canonical_vps])
        #self.assertEqual(len(canonical_vps),len(result_sentences))
        self.assertEqual(list(sorted(result_sentences)),list(sorted([node.full_text for node in canonical_vps])))

    def test_relcl(self):
        text="the women, who stands behind the house, wears a blue tshirt"
        graph=OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        c_tranf = CanonicalizationTransformer()
        c_tranf(graph)

        canonical_sentences=[
            'the women stands behind the house',
            'the women wears a blue tshirt'
        ]

        canonical_vps=graph.fn(type="canonical_vp")

        self.assertEqual(list(sorted(canonical_sentences)),list(sorted([node.full_text for node in canonical_vps])))
        print(graph.fn(type="canonical_vp"))

if __name__=='__main__':
    unittest.main()