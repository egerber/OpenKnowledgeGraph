from __future__ import annotations
from typing import Callable, Any
import collections

from more_itertools import take

MAX_REPR_PREVIEW_ITEMS = 15


class GroupedEntities:

    def __init__(self, graph, entities_by_group):
        self.graph = graph
        self.sorted_entities_by_group = collections.OrderedDict(
            sorted(entities_by_group.items(), key=lambda kv: len(kv[1]), reverse=True))

    def __getitem__(self, item):
        return self.sorted_entities_by_group[item]

    @staticmethod
    def get_type():
        return "GroupedEntities"

    def keys(self):
        return self.sorted_entities_by_group.keys()

    def apply(self, func: Callable[[Any], Any]) -> Any:
        for group, _ in self.sorted_entities_by_group.items():
            func(group)

    def __repr__(self):
        return_string = "<{}: \n".format(self.get_type())
        i = 0
        for group, nodes in self.sorted_entities_by_group.items():
            if i < MAX_REPR_PREVIEW_ITEMS:
                return_string += "{}: {}\n".format(group, len(nodes))
                i += 1
            else:
                break

        if len(self.sorted_entities_by_group) > MAX_REPR_PREVIEW_ITEMS:
            return_string += "...({} more)".format(len(self.sorted_entities_by_group) - MAX_REPR_PREVIEW_ITEMS)

        return return_string

    def get_top_entities(self, k=10):
        return {k: v for k, v in take(k, self.sorted_entities_by_group.items())}

    def top(self, k=10):
        return GroupedEntities(self.graph, self.get_top_entities(k))
