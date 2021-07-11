import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestCanonicalVP(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test1(self):
        graph=OpenKnowledgeGraph()

        graph.create_node("custom",{'prop1':1,'prop2':2})
        


if __name__=='__main__':
    unittest.main()