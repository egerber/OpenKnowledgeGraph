from __future__ import annotations
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.selections.LinkSelection import LinkSelection
from openKnowledgeGraph.selections.NodeSelection import NodeSelection
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class GraphSelection:
    """
    represents a subset of links and nodes from another graph
    """

    def __init__(self, graph, nodes:NodeSelection,links:LinkSelection):
        self.graph : OpenKnowledgeGraph = graph
        self.selected_nodes: NodeSelection=nodes
        self.selected_links: LinkSelection=links

    def get_graph(self)->OpenKnowledgeGraph:
        return self.graph

    @property
    def nodes(self) -> NodeSelection:
        return self.selected_nodes

    @property
    def links(self) -> LinkSelection:
        return self.selected_links
        
    def merge(self,graph_selection:GraphSelection):
        #TODO implement
        pass

    def _clone(self,clone_node_as_reference=False):
        '''
        clone_node_as_reference determines whether node is created using graph.create_node() or graph.create_reference_node()
        '''
        old_id_to_new_id={}

        new_nodes=NodeSelection(self.graph)
        new_links=LinkSelection(self.graph)

        for node in self.selected_nodes:
            if clone_node_as_reference:
                cloned_node=self.graph.create_reference_node(reference_node=node,node_type=node.type, properties=node.get_properties())
            else:
                cloned_node=self.graph.create_node(node_type=node.type, properties=node.get_properties())
            old_id_to_new_id[node.get_id()]=cloned_node.get_id()
            new_nodes.append(cloned_node)

        for link in self.selected_links:
            source_node=self.graph.get_node(old_id_to_new_id[link.source_id])
            target_node=self.graph.get_node(old_id_to_new_id[link.target_id])
            cloned_link=self.graph.create_link(
                link_type=link.type,
                source=source_node,
                target=target_node,
                **link.get_properties()
            )

            new_links.append(cloned_link)

        return GraphSelection(graph=self.graph,nodes=new_nodes,links=new_links)

    def filter_nodes(self,query=None, **query_args) -> GraphSelection:
        '''
        returns a filtered GraphSelection for given node query
        excludes links from selection that have 'broken' connection(no connection to both source node and target node)
        '''

        filtered_nodes=self.selected_nodes.filter(query=None, **query_args)

        #filter links that reference filtered node
        filtered_node_ids=filtered_nodes.id
        filtered_links=self.selected_links.filter(
            Q(target_id__in=filtered_node_ids) & Q(source_id__in=filtered_node_ids)
        )

        return GraphSelection(graph=self.graph,nodes=filtered_nodes, links=filtered_links)

    def filter_links(self,query=None, **query_args) -> GraphSelection:
        '''
        returns a filtered GraphSelection for the given link query
        excludes nodes from selection that are not referenced by links
        '''
        filtered_links=self.selected_links.filter(query=query,**query_args)

        #filter nodes that are connected to one or many filtered links
        filtered_link_adjacent_nodes=filtered_links.nodes
        filtered_nodes=self.selected_nodes.intersect(filtered_link_adjacent_nodes)

        return GraphSelection(graph=self.graph,nodes=filtered_nodes, links=filtered_links)
    
    def clone(self) -> GraphSelection:
        '''
        produces duplicate of all nodes and links in the selection (new links reference new nodes)
        '''
        return self._clone(clone_node_as_reference=False)
        
    
    def clone_with_references(self) -> GraphSelection:
        '''
        produces duplicates of all nodes and links, but with nodes that reference the original nodes while links connect newly created nodes
        '''
        return self._clone(clone_node_as_reference=True)


    def count(self) -> int:
        return len(self.selected_nodes) + len(self.selected_links)

    def __repr__(self):
        return "<GraphSelection with {} nodes and {} links>".format(len(self.selected_nodes),
                                                                          len(self.selected_links))
