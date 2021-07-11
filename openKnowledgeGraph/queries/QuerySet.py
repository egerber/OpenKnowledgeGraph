'''
taken from
https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/queryset/visitor.py
'''
from openKnowledgeGraph.queries.FilterOperations import filter_entities_by_single_filter
from openKnowledgeGraph.utils.listutils import unique_items

AND_OP = 0
OR_OP = 1


class QNode:
    """Base class for nodes in query trees."""

    AND = 0
    OR = 1

    def _combine(self, other, operation):
        """Combine this node with another node into a QCombination
        object.
        """
        # If the other Q() is empty, ignore it and just use `self`.
        if not bool(other):
            return self

        # Or if this Q is empty, ignore it and just use `other`.
        if not bool(self):
            return other

        return QCombination(operation, [self, other])

    def __or__(self, other):
        return self._combine(other, OR_OP)

    def __and__(self, other):
        return self._combine(other, AND_OP)


class QCombination(QNode):
    """Represents the combination of several conditions by a given
    logical operator.
    """

    def __init__(self, operation, children):
        self.operation = operation
        self.children = []
        for node in children:
            # If the child is a combination of the same type, we can merge its
            # children directly into this combinations children
            if isinstance(node, QCombination) and node.operation == operation:
                self.children += node.children
            else:
                self.children.append(node)

    def __repr__(self):
        op = " & " if self.operation is self.AND else " | "
        return "(%s)" % op.join([repr(node) for node in self.children])

    def __call__(self, selection):
        if self.operation == AND_OP:  # PATH
            filtered_selection = selection
            for child in self.children:
                filtered_selection = child(filtered_selection)
        else:  # OR PATH
            filtered_selection = None
            for child in self.children:
                if filtered_selection is None:
                    filtered_selection = child(selection)
                else:
                    # union two lists (could be more efficiently in the future using dicts ={id -> node}
                    filtered_selection = unique_items(filtered_selection + child(selection))

        return filtered_selection

    def __bool__(self):
        return bool(self.children)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__
                and self.operation == other.operation
                and self.children == other.children
        )


class Q(QNode):
    """A simple query object, used in a query tree to build up more complex
    query structures.
    """

    def __init__(self, **query):
        self.query = query

    def __call__(self, entities):
        filtered_nodes = entities
        for key, value in self.query.items():
            if key == 'entities':
                continue

            filtered_nodes = filter_entities_by_single_filter(filtered_nodes, key, value)

        return filtered_nodes

    def __repr__(self):
        return "Q(**%s)" % repr(self.query)

    def __bool__(self):
        return bool(self.query)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.query == other.query
