import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestTokenNode(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_properties1(self):
        text='''In machine learning and natural language processing, a topic model is a type of statistical model
         for discovering the abstract topics that occur in a collection of documents
        '''
        graph = OpenKnowledgeGraph.from_text(text, model='en_core_web_sm')

        tokens=graph.fn(type="token")

        nsubj=tokens.graph.fn(type="token",dep="nsubj").first()
        root=tokens.graph.fn(type="token",dep="root").first()

        self.assertEqual(nsubj.voice,"active")
        self.assertEqual(nsubj.number, "singular")
        self.assertEqual(root.tense,"present")
        self.assertEqual(root.negated,False)
        self.assertEqual(root.i,11)
        self.assertEqual(root.lemma,'be')
        self.assertEqual(root.text,'is')
        self.assertEqual(root.tag,'vbz')
        self.assertEqual(root.pos,'aux')

        self.assertEqual(tokens.count(),31)

    def test_properties2(self):
        text='''We did not get introduced to the man with the white jacket'''
        graph = OpenKnowledgeGraph.from_text(text, model='en_core_web_sm')

        tokens=graph.fn(type="token")

        nsubjpass=tokens.graph.fn(type="token",dep="nsubjpass").first()
        root=tokens.graph.fn(type="token",dep="root").first()

        #computed properties
        self.assertEqual(nsubjpass.voice,"passive")
        self.assertEqual(nsubjpass.number, "plural")
        self.assertEqual(root.tense,"past")
        self.assertEqual(root.negated,True)
        
        #static properties
        self.assertEqual(root.i,4)
        self.assertEqual(root.tag,'vbn')
        self.assertEqual(root.dep,'root')
        self.assertEqual(root.pos,'verb')
        self.assertEqual(root.text,'introduced')
        self.assertEqual(nsubjpass.i,0)
        self.assertEqual(root.whitespace,' ')
        self.assertEqual(tokens.count(),12)


        self.assertEqual(root.i, root.get_property("i"))
        self.assertEqual(root.dep,root.get_property("dep"))
        self.assertEqual(root.pos, root.get_property("pos"))

    def test_properties3(self):
        text='Steve Jobs founded Apple'
        graph=OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        token_node=graph.fn(type="token").first()
        self.assertEqual(token_node.has_property("text"),True)
        self.assertEqual(token_node.has_property("dep"),True)
        self.assertEqual(token_node.has_property("full_text"),True)


if __name__=='__main__':
    unittest.main()