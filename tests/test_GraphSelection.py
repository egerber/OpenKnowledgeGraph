from openKnowledgeGraph.queries.QuerySet import Q
import unittest

from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class TestGraphSelection(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def test_clone(self):
        text="This is a test sentence, that I came up with"
        graph : OpenKnowledgeGraph=OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        token=graph.fn(type="token",dep="root").first()
        graph_selection=token.traverse_graph_by_out_links(Q(type="dependency"))
        
        count_nodes_before=graph.fn().count()
        count_links_before=graph.fl().count()
        nodes_in_selection=graph_selection.nodes.count()
        links_in_selection=graph_selection.links.count()

        graph_selection.clone()
        self.assertEqual(count_nodes_before+nodes_in_selection,graph.fn().count())
        self.assertEqual(count_links_before+links_in_selection,graph.fl().count())

    def test_clone_with_reference(self):
        text="This is a test sentence, that I came up with"
        graph : OpenKnowledgeGraph=OpenKnowledgeGraph.from_text(text,model='en_core_web_sm')

        token=graph.fn(type="token",dep="root").first()
        graph_selection=token.traverse_graph_by_out_links(Q(type="dependency"))
        
        count_nodes_before=graph.fn().count()
        count_links_before=graph.fl().count()
        nodes_in_selection=graph_selection.nodes.count()
        links_in_selection=graph_selection.links.count()

        graph_selection.clone_with_references()
        self.assertEqual(count_nodes_before+nodes_in_selection,graph.fn().count())
        self.assertEqual(count_links_before+links_in_selection+nodes_in_selection,graph.fl().count())


    def test_filter_nodes(self):
        graph : OpenKnowledgeGraph=OpenKnowledgeGraph()
        
        node1=graph.create_node("custom")
        node2=graph.create_node("custom")
        node3=graph.create_node("custom")
        
        link1=graph.create_link("c",node1,node2)
        link2=graph.create_link("c",node2,node3)
        link3=graph.create_link("c",node3,node1)

        graph_selection=node1.traverse_graph_by_out_links()
        self.assertEqual(graph_selection.nodes.count(),3)
        self.assertEqual(graph_selection.links.count(),3)

        graph_selection2=graph_selection.filter_nodes(id=node1.id)
        self.assertEqual(graph_selection2.nodes[0].id,node1.id)
        self.assertEqual(graph_selection2.links.count(),0)

        graph_selection3=graph_selection.filter_nodes(id__in=[node1.id, node2.id])
        self.assertEqual(graph_selection3.nodes.id,[node1.id, node2.id])
        self.assertEqual(graph_selection3.links.count(),1)
        self.assertEqual(graph_selection3.links[0].id,link1.id)

    def test_filter_links(self):
        graph : OpenKnowledgeGraph=OpenKnowledgeGraph()
        
        node1=graph.create_node("custom")
        node2=graph.create_node("custom")
        node3=graph.create_node("custom")
        node4=graph.create_node("custom")
        
        link1=graph.create_link("c",node1,node2)
        link2=graph.create_link("c",node2,node3)
        link3=graph.create_link("c",node3,node4)

        graph_selection=node1.traverse_graph_by_out_links()

        graph_selection2=graph_selection.filter_links(id=link1.id)
        self.assertEqual(graph_selection2.links.id,[link1.id])
        self.assertEqual(sorted(graph_selection2.nodes.id),sorted([node1.id,node2.id]))

        graph_selection3=graph_selection.filter_links(id__in=[link1.id, link2.id])
        self.assertEqual(sorted(graph_selection3.nodes.id),sorted([node1.id, node2.id,node3.id]))
        self.assertEqual(sorted(graph_selection3.links.id),sorted([link1.id, link2.id]))

if __name__=='__main__':
    unittest.main()