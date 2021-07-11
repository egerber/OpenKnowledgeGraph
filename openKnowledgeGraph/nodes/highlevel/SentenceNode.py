from openKnowledgeGraph.nodes.Node import Node


class SentenceNode(Node):

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @staticmethod
    def get_type():
        return "sentence"

    @staticmethod
    def from_spacy_sent(graph, sent):
        sentence_node = SentenceNode(text=sent.text)
        graph.add_node(sentence_node)

        return sentence_node
