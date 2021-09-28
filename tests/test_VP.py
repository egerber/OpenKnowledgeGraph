import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestVP(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_fulltext1(self):
        texts = [
            'Steve Jobs and Paul Wozniac founded Apple.',
            'Once upon the time there was a little bear...',
            'In 2004, they year after 2003, they had the biggest sandstorm in the history.'
        ]
        
        for text in texts:
            graph = OpenKnowledgeGraph.from_text(text, model='en_core_web_sm')

            root=graph.fn(type="token",dep="root").first()
            self.assertEqual(root.full_text,text)


if __name__=='__main__':
    unittest.main()