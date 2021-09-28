from openKnowledgeGraph.queries.QuerySet import Q
import unittest
import spacy

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestEntityLinker(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def test_initialize(self):
        text="Abraham Lincoln was a president of the United States of America"

        graph=OpenKnowledgeGraph.from_text(text=text,model='en_core_web_sm',components=['token','dependency','constituent','entity_linker'])

 

if __name__=='__main__':
    unittest.main()