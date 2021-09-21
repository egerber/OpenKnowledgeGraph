import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.transformers.TransformerGroup.CanonicalizationTransformer import CanonicalizationTransformer


class TestConstituents(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test1(self):
        text = 'Apples and tomatoes are red'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        np_nodes=graph.fn(type="np")
        vp_nodes=graph.fn(type="vp")

        print(vp_nodes)
        print(graph.fn())
        nps_groundtruth=['tomatoes','Apples','Apples and tomatoes']

        nps_graph=[np.full_text for np in np_nodes]

        self.assertEqual(list(sorted(nps_groundtruth)), list(sorted(nps_graph)))
        self.assertEqual(np_nodes.count(), len(nps_groundtruth))
        self.assertEqual(vp_nodes.count(),1)

if __name__=='__main__':
    unittest.main()