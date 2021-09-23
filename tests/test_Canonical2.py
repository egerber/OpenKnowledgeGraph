from openKnowledgeGraph.transformers.ConstituentTransformer2 import ConstituentTransformer2
import unittest
from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.CanonicalizationTransformer2 import CanonicalizationTransformer2


class TestCanonical2(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_np(self):
        text='apples and tomatoes are red'#, and oranges are orange and juicy. Bill Gates is an entrepreneur.'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm',components=['token','dependency'])

        constituent_transformer2=ConstituentTransformer2()
        constituent_transformer2(graph)

        canonical_transformer=CanonicalizationTransformer2()
        canonical_transformer(graph)

        canonical_phrases=[
            'apples are red',
            'tomatoes are red',
            'oranges are orange',
            'oranges are juicy',
            'Bill Gates is an entreprenur'
        ]

        self.assertEqual(
            list(sorted(graph.fn(type="canonical2").full_text)),
            list(sorted(canonical_phrases))
        )

if __name__=='__main__':
    unittest.main()