from collections import defaultdict
from openKnowledgeGraph.nodes.Node import Node
from typing import List

class NodeDictionary:

    def __init__(self):
        self.nodes_by_id = {}

        self.innodes_by_node_id = defaultdict(list)
        self.outnodes_by_node_id = defaultdict(list)

    def add(self, node, override_if_exists=False):
        pass

    def __getitem__(self, node_id):
        return self.nodes_by_id[node_id]

    def __setitem__(self,node_id,item):
        self.nodes_by_id[node_id]=item

    def __contains__(self, item):
        return item in self.nodes_by_id

    def __len__(self):
        return len(self.nodes_by_id)

    def get_nodes(self,node_ids=None) -> List[Node]:
        '''
        returns node objects
        if node_ids is None returns all nodes
        if node_ids is list of ids, returns nodes by id
        '''
        if node_ids is None:
            return list(self.nodes_by_id.values())
        else:
            return [self.nodes_by_id[id] for id in node_ids]

    def get_outnodes_for_node(self, node):
        return self.outnodes_by_node_id[node.get_id()]

    def remove(self, node) -> None:
        node_id = node.get_id()
        node = self.nodes_by_id[node_id]
        if node is None:
            return

        del self.nodes_by_id[node_id]

    @staticmethod
    def create_from_nodes(nodes):
        node_dictionary = NodeDictionary()
        for node in nodes:
            node_dictionary.add(node)

        return node_dictionary
