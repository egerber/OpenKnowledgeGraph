import os

from openKnowledgeGraph.queries.QuerySet import Q

DEBUG = os.environ.get('DEBUG', False)


class GraphOperation:

    pattern_based=True #TODO maybe add two subclasses for pattern based vs input based graph operations

    def __init__(self, apply=None, pattern=None, **kwargs):
        self.limit = kwargs.get('limit', None)

        self.func_apply = apply
        self.custom_pattern = pattern

        self.applied_operations=[]

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
        '''
        name of the component, needs to be overriden
        '''
        raise NotImplementedError()

    def __call__(self, graph, *args, **kwargs):
        self.check_dependencies(graph)
        candidates = self.find_candidate_nodes(graph)

        returned_values = []
        for candidate in candidates:
            returned_values.append(self._apply(candidate,*args, **kwargs))

        self.register_self(graph)

        return self.after_apply(candidates, returned_values)

    def check_dependencies(self,graph):
        for dependency in self.get_dependencies():
            if not graph.has_component(dependency):
                raise ValueError("dependency '{}' could not be found but is a dependency for '{}'".format(dependency,self.get_name()))

    def register_self(self,graph):
        graph.register_component(self.get_name())

    @staticmethod
    def get_dependencies():
        return []
