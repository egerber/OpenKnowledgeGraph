from openKnowledgeGraph.transformers.ConstituentTransformer import ConstituentTransformer
import unittest
from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.CanonicalizationTransformer import CanonicalizationTransformer


class TestCanonical(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_graph_for_text(self, text):
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm',components=['token'])

        constituent_transformer2=ConstituentTransformer()
        constituent_transformer2(graph)

        canonical_transformer=CanonicalizationTransformer()
        canonical_transformer(graph)

        return graph

    def test_nsubj_conjuncts(self):
        graph=self.get_graph_for_text(text='apples and tomatoes are red')

        canonical_phrases=[
            'apples are red',
            'tomatoes are red',
        ]

        self.assertEqual(
            list(sorted(graph.fn(type="canonical").full_text)),
            list(sorted(canonical_phrases))
        )

    def test_vp_conjunctions(self):
        graph=self.get_graph_for_text(text="Paul was a programmer and Tom is a clerk")

        canonical_phrases=[
            'Paul was a programmer ',
            'Tom is a clerk',
        ]

        self.assertEqual(
            list(sorted(graph.fn(type="canonical").full_text)),
            list(sorted(canonical_phrases))
        )

    def test_attr_conjunctions(self):
        graph=self.get_graph_for_text(text='Steve and Paul founded a company and became successful and rich')

        canonical_phrases=[
            'Steve founded a company ',
            'Paul founded a company ',
            'Steve became successful ',
            'Paul became successful ',
            'Steve became rich',
            'Paul became rich'
        ]

        self.assertEqual(
            list(sorted(graph.fn(type="canonical").full_text)),
            list(sorted(canonical_phrases))
        )

    def test_attr(self):
        graph=self.get_graph_for_text(text='Steve and Paul became successful and rich')
        
        canonical_phrases=[
            'Steve became successful ', 
            'Steve became rich', 
            'Paul became successful ', 
            'Paul became rich'
        ]

        self.assertEqual(
            list(sorted(graph.fn(type="canonical").full_text)),
            list(sorted(canonical_phrases))
        )

    def test_vp(self):
        graph=self.get_graph_for_text(text='Steve and Paul founded a company and became successful')

        canonical_phrases=[
            'Steve founded a company ', 
            'Paul founded a company ', 
            'Steve became successful', 
            'Paul became successful'
        ]

        self.assertEqual(
            sorted(graph.fn(type="canonical").full_text),
            sorted(canonical_phrases)
        )
        
    def test_relcl(self):
        graph=self.get_graph_for_text(text="the women, who stands behind the house, wears a blue tshirt")
        canonical_sentences=[
            'the women stands behind the house',
            'the women wears a blue tshirt'
        ]

        self.assertEqual(
            sorted(canonical_sentences),
            sorted(graph.fn(type="canonical").full_text)
        )

    def test_wiki_mccartney(self):
        '''
        testing if anything breaks with longer, more complex input
        '''
        with open('sample_texts/mccartney.txt', 'r') as f:
            text = ''.join(f.readlines())
            
            graph=self.get_graph_for_text(text)

            print(graph.fn(type="canonical").full_text)

    def test_wiki_rickmorty(self):
        '''
        testing if anything breaks with longer, more complex input
        '''
        with open('sample_texts/rickmorty.txt', 'r') as f:
            text = ''.join(f.readlines())
            
            graph=self.get_graph_for_text(text)

            print(graph.fn(type="canonical").full_text)
        
        
if __name__=='__main__':
    unittest.main()