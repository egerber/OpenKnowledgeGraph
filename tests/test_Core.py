from openKnowledgeGraph.queries.QuerySet import Q
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

    def test_set_and_get_attributes(self):
        graph=OpenKnowledgeGraph()
        original_node=graph.create_node(
            node_type="custom_node_type",
            properties={'attr1':1,'attr2':2})
        
        self.assertEqual(original_node.__getattr__('attr1'),1)
        self.assertEqual(original_node.__getattr__('attr2'),2)


    def test_create_from_text(self):
        text="This is an example text, including special characters such as numbers (1,2,3), and other things. This is the second sentence"
        
        nlp=spacy.load('en_core_web_sm')
        doc=nlp(text)
        num_tokens=len(doc)

        graph=OpenKnowledgeGraph.from_text(text=text,model='en_core_web_sm')

        self.assertEqual(graph.fn(type="token").count(),num_tokens)
        self.assertEqual(graph.fn(type="sentence").count(),len(list(doc.sents)))
        self.assertEqual(graph.fn(type="document").count(),1)
 
    def test_dependencies(self):
        text="This is an example text, including special characters such as numbers (1,2,3), and other things. This is the second sentence"
        graph=OpenKnowledgeGraph.from_text(text=text)

    def test_find_nodes(self):
        text = 'Steve Jobs and Steve Wozniac founded Apple'
        graph = OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        self.assertEqual(graph.fn(type="token",tense="past").count(),1)


    def test_properties(self):
        graph=OpenKnowledgeGraph()
        properties={
            'prop1':'a',
            'prop2':12,
            'prop3':-1
        }
        new_node=graph.create_node(node_type="custom_node",properties=properties)

        self.assertEqual(new_node.get_properties(),properties)

    def test_clone(self):
        graph=OpenKnowledgeGraph()
        node=graph.create_node(node_type="custom",properties={'prop1':1,'prop2':'2'})
        cloned_node=graph.find_nodes(id=node.id).clone().first()
        
        self.assertEqual(cloned_node.get_properties(),node.get_properties())

    def test_link_properties(self):
        graph=OpenKnowledgeGraph()
        node1=graph.create_node(node_type="custom",properties={'prop1':1,'prop2':'2'})
        node2=graph.create_node(node_type="custom",properties={'prop1':1,'prop2':'2'})
        link=graph.create_link(link_type="custom_link",source=node1,target=node2,prop1=10)

        self.assertEqual(node1.type,"custom")

    def test_nested_properties(self):
        graph=OpenKnowledgeGraph()
        node1=graph.cn(node_type="custom",properties={'text':'Hello world!'})
        node2=graph.cn(node_type="custom")
        node2.set_nested_property("testfield",node1)
        self.assertEqual(node2.get_property("testfield__text"),"Hello world!")
        self.assertEqual(node2.testfield,node1)
        self.assertEqual(node2.testfield.text,"Hello world!")
        self.assertEqual(node2.get_property("nonexistentfield__text"),None)

if __name__=='__main__':
    unittest.main()