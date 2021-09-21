import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestSentenceSplitting(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_create(self):
        graph=OpenKnowledgeGraph()
        original_node=graph.create_node(node_type="custom_node_type",properties={'attr1':1,'attr2':2})
        reference_node=graph.create_reference_node(
            reference_node=original_node,
            node_type="custom_reference_node",
            properties={'attr2':3,'attr3':4})

        self.assertEqual(original_node.__getattr__('attr1'),1)
        self.assertEqual(original_node.__getattr__('attr2'),2)
        self.assertEqual(reference_node.__getattr__('attr1'),1)
        self.assertEqual(reference_node.__getattr__('attr2'),3)
        self.assertEqual(reference_node.__getattr__('attr3'),4)

if __name__=='__main__':
    unittest.main()