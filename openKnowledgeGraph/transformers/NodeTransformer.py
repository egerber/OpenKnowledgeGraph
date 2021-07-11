import os

from openKnowledgeGraph.queries.QuerySet import Q

DEBUG = os.environ.get('DEBUG', False)


class NodeTransformer:

    def __init__(self, apply=None, pattern=None, **kwargs):
        self.limit = kwargs.get('limit', None)

        self.func_apply = apply
        self.custom_pattern = pattern

    def find_candidate_nodes(self, graph):
        selection = graph.find_nodes(self._get_pattern())
        if self.limit is not None:
            return selection.limit(self.limit)
        else:
            return selection

    def is_candidate(self, node):
        return node.matches(self.get_pattern())

    def get_pattern(self):
        return Q()

    def _get_pattern(self):
        if self.custom_pattern is not None:
            return self.custom_pattern
        else:
            return self.get_pattern()

    def _apply(self, node, *args, **kwargs):
        if self.func_apply is not None:
            # use overridden function
            return self.func_apply(node, *args, **kwargs)
        else:
            return self.apply(node, *args, **kwargs)

    def apply(self, node, *args, **kwargs):
        return None

    @staticmethod
    def get_name():
        return "BaseNodeTransformer"

    def __call__(self, graph):
        candidates = self.find_candidate_nodes(graph)
        if DEBUG:
            print("found {} candidates".format(len(candidates)))
            print(candidates)

        new_nodes = []
        for candidate in candidates:
            returned_nodes = self._apply(candidate)
            if returned_nodes is None:
                continue
            elif isinstance(returned_nodes, list):
                new_nodes += returned_nodes
            else:
                new_nodes.append(returned_nodes)

        if DEBUG:
            print("added {} nodes".format(len(new_nodes)))

        return new_nodes
