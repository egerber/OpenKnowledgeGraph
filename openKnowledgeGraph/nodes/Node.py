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

    def get_properties(self):
        pass

    def add_property(self, property):
        pass

    def __repr__(self):
        return "<Node ({}): {}>".format(self.get_type(), self.get_text())

    def get_decorator_nodes(self):
        return self.find_in_links(type="decorator").source_nodes

    def __getattr__(self, name):
        if name.startswith('attr__'):
            return self.get_attribute(name[6:])
        else:
            try:
                return self.__getattribute__(name)
            except:
                decorators = self.get_decorator_nodes()
                for decorator in decorators:
                    decorator_attribute = decorator.__getattr__(name)
                    if decorator_attribute:
                        return decorator_attribute
                return None  # default return if attribute does not exist

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
        return LinkSelection(self.get_graph(), self._get_links_list(*queries, **query_args))

    def find_link(self, *queries, **query_args):
        links = LinkSelection(self.get_graph(), self._get_links_list(*queries, **query_args))
        if len(links) > 0:
            return links[0]
        else:
            return None

    def find_in_links(self, *queries, **query_args):
        return LinkSelection(self.get_graph(), self._get_in_links_list(*queries, **query_args))

    def find_out_links(self, *queries, **query_args):
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
