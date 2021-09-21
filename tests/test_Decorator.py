import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestDecorator(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test1(self):
        graph=OpenKnowledgeGraph()

        original_node=graph.create_node("custom",{'prop1':1,'prop2':2})
        decorator_node=graph.create_decorator_node(
            source_node=original_node,
            node_type="custom_decorator",
            properties={'prop2':-2,'prop3':3})

        self.assertEqual(original_node.get_property("prop1"),1)
        self.assertEqual(original_node.get_property("prop2"),2)
        self.assertEqual(original_node.get_property("prop3"),3)


if __name__=='__main__':
    unittest.main()