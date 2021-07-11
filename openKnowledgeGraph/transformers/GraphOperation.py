import os

from openKnowledgeGraph.queries.QuerySet import Q

DEBUG = os.environ.get('DEBUG', False)


class GraphOperation:

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
        '''
        hook that is called for each element
        optionally can return a value which will be stored for all nodes
        :param node:
        :param args:
        :param kwargs:
        :return:
        '''
        return None

    def after_apply(self, nodes, returned_values, *args, **kwargs):
        '''
        hook that is called after apply() was called on each element
        overrides return value of GraphOperation
        :param nodes:
        :param returned_values:
        :param args:
        :param kwargs:
        :return:
        '''

        # by default filters out None and flattens elements
        _returned_values = []
        for value in returned_values:
            if value is None:
                continue
            elif isinstance(value, list):
                _returned_values += value
            else:
                _returned_values.append(value)

        return _returned_values

    @staticmethod
    def get_name():
        return "BaseNodeTransformer"

    def __call__(self, graph):
        candidates = self.find_candidate_nodes(graph)
        if DEBUG:
            print("found {} candidates".format(len(candidates)))
            print(candidates)

        returned_values = []
        for candidate in candidates:
            returned_values.append(self._apply(candidate))

        return self.after_apply(candidates, returned_values)


    @staticmethod
    def get_dependencies():
        '''TODO check if '''
        return []
