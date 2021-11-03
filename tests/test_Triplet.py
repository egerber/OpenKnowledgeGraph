import unittest
from openKnowledgeGraph.transformers.ConstituentTransformer import ConstituentTransformer
from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.CanonicalizationTransformer import CanonicalizationTransformer
from openKnowledgeGraph.transformers.TripletTransformer import TripletTransformer


class TestTriplet(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_graph_for_text(self, text):
        graph = OpenKnowledgeGraph.from_text(text, model='en_core_web_sm', components=['token'])

        constituent_transformer2 = ConstituentTransformer()
        constituent_transformer2(graph)

        canonical_transformer = CanonicalizationTransformer()
        canonical_transformer(graph)

        triplet_transformer = TripletTransformer()
        triplet_transformer(graph)

        return graph

    def test_example1(self):
        graph = self.get_graph_for_text("Tom likes tomatoes")

        triplet_selection = graph.fn(type="triplet")
        self.assertEqual(triplet_selection.count(), 1)

        triplet = triplet_selection.first()
        self.assertEqual(triplet.subject__text, "Tom")
        self.assertEqual(triplet.predicate__text, "likes")
        self.assertEqual(triplet.object__text, "tomatoes")

    def test_wikipedia1(self):
        with open('sample_texts/mccartney.txt', 'r') as f:
            text = ''.join(f.readlines())
            
            graph=self.get_graph_for_text(text)
            triplet_selection=graph.fn(type="triplet")
            for triplet in triplet_selection:
                print(f'{triplet.subject.full_text} - {triplet.predicate.text} - {triplet.object.full_text}')

if __name__ == '__main__':
    unittest.main()
