import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestDependency(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test1(self):
        text = 'Apples and tomatoes are red'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        self.assertEqual(graph.fn(type="dependency").count(),7)
    
    def test2(self):
        pass

if __name__=='__main__':
    unittest.main()