from openKnowledgeGraph.nodes.Node import Node


class DocumentNode(Node):

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)

    @staticmethod
    def get_type():
        return "document"

    @staticmethod
    def from_spacy_doc(graph, doc):
        document_node = graph.create_node(node_type="document",properties={'text':doc.text})
        graph.add_node(document_node)

        return document_node
