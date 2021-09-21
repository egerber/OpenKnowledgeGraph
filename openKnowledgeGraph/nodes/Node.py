from openKnowledgeGraph.Entity import Entity
from openKnowledgeGraph.nodes import NodeRegistry
from openKnowledgeGraph.selections.LinkSelection import LinkSelection
from openKnowledgeGraph.selections.NodeSelection import NodeSelection
from openKnowledgeGraph.utils.listutils import unique_items


class Node(Entity):

    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)

    def _get_in_links_list(self, *queries, **query_args):
        """
        get all links that reference node as target
        """
        return self.get_graph().get_inlinks_for_node(self, *queries, **query_args)

    def _get_links_list(self, *queries, **query_args):
        return self.get_graph().get_links_for_node(self, *queries, **query_args)

    def _get_out_links_list(self, *queries, **query_args):
        """
        get all links that reference node as source
        """
        return self.get_graph().get_outlinks_for_node(self, *queries, **query_args)

    def __repr__(self):
        return "<Node ({}): {}>".format(self.type, self.get_text())

    def has_reference_node(self):
        return self.find_out_links(type="reference").count()>0

    def get_reference_node(self):
        return self.find_out_links(type="reference").target_nodes[0]

    def get_decorator_nodes(self):
        return self.find_in_links(type="decorator").source_nodes

    def set_property(self,key,value):
        self.graph.set_property_for_node(self.id,key,value)

    def get_property(self,name):
        '''
        tries to resolve properties in the order
        - registered(static) properties
        - computed properties (@property methods)
        - reference node properties
        - decorated properties
        '''

        if self.graph.node_has_property(self.id,name):
            #static properties
            return self.graph.get_property_for_node(self.id,name)
        elif self.has_computed_property(name):
            #computed properties
            return self.__getattribute__(name)
        elif self.has_reference_node() and self.get_reference_node().has_property(name):
            #reference nodes
            return self.get_reference_node().get_property(name)
        for decorator_node in self.get_decorator_nodes():
            #decorator nodes
            if decorator_node.has_property(name):
                return decorator_node.get_property(name)
        
    def get_properties(self) -> dict:
        return self.graph.get_properties_for_node(self.get_id())

    def has_property(self,key):
        if self.graph.node_has_property(self.id,key):
            return True
        elif self.graph.node_has_computed_property(self.id,key):
            return True
        elif self.has_reference_node():
            return self.get_reference_node().has_property(key)
        else:
            for decorator_node in self.get_decorator_nodes():
                if decorator_node.has_property(key):
                    return True

        return False

    def __getattr__(self, name):
        return self.get_property(name)

    def _get_out_nodes_list(self):
        out_nodes = []
        for link in self.out_links:
            out_nodes.append(link.target)

        return unique_items(out_nodes)

    def _get_in_nodes_list(self):
        in_nodes = []
        for link in self.in_links:
            in_nodes.append(link.source)

        return unique_items(in_nodes)

    def _get_adjacent_nodes_list(self):
        adjacent_nodes = []
        for link in self.links:
            adjacent_nodes.append(link.source)
            adjacent_nodes.append(link.target)

        return unique_items(adjacent_nodes)

    @property
    def in_nodes(self):
        return NodeSelection(self.get_graph(), self._get_in_nodes_list())

    @property
    def adjacent_nodes(self):
        return NodeSelection(self.get_graph(), self._get_adjacent_nodes_list())

    @property
    def links(self):
        return self.get_graph().get_links_for_node(self)

    @property
    def in_links(self):
        return LinkSelection(self.get_graph(), self._get_in_links_list())

    @property
    def out_nodes(self):
        return NodeSelection(self.get_graph(), self._get_out_nodes_list())

    @property
    def out_links(self):
        return LinkSelection(self.get_graph(), self._get_out_links_list())

    def find_links(self, *queries, **query_args):
        '''
        returns queried LinkSelection of all inlinks and outlinks
        '''
        return LinkSelection(self.get_graph(), self._get_links_list(*queries, **query_args))


    def find_in_links(self, *queries, **query_args):
        '''
        returns queried LinkSelection of all inlinks
        '''
        return LinkSelection(self.get_graph(), self._get_in_links_list(*queries, **query_args))

    def find_out_links(self, *queries, **query_args):
        '''
        returns queried LinkSelection of all outlinks
        '''
        return LinkSelection(self.get_graph(), self._get_out_links_list(*queries, **query_args))

    def find_in_nodes(self, *queries, **query_args):
        return self.in_nodes.filter(*queries, **query_args)

    def find_out_nodes(self, *queries, **query_args):
        return self.out_nodes.filter(*queries, **query_args)

    def find_adjacent_nodes(self, *queries, **query_args):
        return self.adjacent_nodes.filter(*queries, **query_args)

    def _traverse_by_out_links(self, max_depth, traversed_selection, query):
        if max_depth is None:
            pass
        elif max_depth < 0:
            return
        traverse_out_nodes = self.find_out_links(*[query]).target_nodes
        for node in traverse_out_nodes:
            traversed_selection.append(node)
            node._traverse_by_out_links(max_depth=max_depth - 1, traversed_selection=traversed_selection, query=query)

    def traverse_by_out_links(self, max_depth=20, query=None):
        traversed_selection = NodeSelection(self.get_graph(), [self])
        self._traverse_by_out_links(max_depth=max_depth, traversed_selection=traversed_selection, query=query)
        return traversed_selection

    def serialize(self):
        return {
            "id": self.get_id(),
            "inlinks": len(self._get_in_links_list()),
            "outlinks": len(self._get_out_links_list()),
            "type": self.get_type(),
            "text": self.get_text(),
            "attribute": {key: value for key, value in self.get_attributes().items()}
        }

    @staticmethod
    def create(node_type, **kwargs):
        NodeClass = NodeRegistry.get_by_type(node_type)

        if NodeClass is not None:
            return NodeClass(**kwargs)
        else:
            from openKnowledgeGraph.nodes.CustomNode import CustomNode
            return CustomNode(node_type, **kwargs)
