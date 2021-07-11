import unittest
import spacy

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_init(self):
        graph=OpenKnowledgeGraph()
        
        self.assertNotEqual(graph,None)

    def test_create_node(self):
        graph=OpenKnowledgeGraph()

        node=graph.create_node("custom",{'prop1':1,'prop2':'property2','prop3':[1,2,3]})
        self.assertEqual(graph.fn(type="custom").count(),1)

    def test_create_link(self):
        graph=OpenKnowledgeGraph()
        src_node=graph.create_node("custom")
        target_node=graph.create_node("custom")

        link=graph.create_link("custom",source=src_node, target=target_node)

        self.assertEqual(graph.fl(type="custom").count(),1)
    
    def test_save_and_restore(self):
        pass

    def test_create_from_text(self):
        text="This is an example text, including special characters such as numbers (1,2,3), and other things. This is the second sentence"
        
        nlp=spacy.load('en_core_web_md')
        doc=nlp(text)
        num_tokens=len(doc)

        graph=OpenKnowledgeGraph.from_text(text=text,model='en_core_web_md')

        self.assertEqual(graph.fn(type="token").count(),num_tokens)
        self.assertEqual(graph.fn(type="sentence").count(),len(list(doc.sents)))
        self.assertEqual(graph.fn(type="document").count(),1)


if __name__=='__main__':
    unittest.main()