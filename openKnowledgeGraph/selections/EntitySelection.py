from __future__ import annotations
from collections import defaultdict
from openKnowledgeGraph.utils.listutils import unique_items
from typing import Callable, Any, List

from openKnowledgeGraph.Entity import Entity
from openKnowledgeGraph.queries.QueryHelper import filter_entities
from openKnowledgeGraph.selections.GroupedEntities import GroupedEntities

MAX_PREVIEW_ITEMS = 10


class EntitySelection:

    def __init__(self, graph, selected_entities=None):
        if selected_entities is None:
            selected_entities=[]
        
        self.graph = graph
        
        #create unique entities
        self.selected_entities = unique_items(selected_entities)

    def __iter__(self):
        for entity in self.selected_entities:
            yield entity

    def get_graph(self):
        return self.graph

    def first(self):
        '''
        returns first element if exists, otherwise returns none
        :return:
        '''
        if len(self) > 0:
            return self[0]
        else:
            return None

    def get_entities(self):
        return self.selected_entities

    def create_selection(self, items):
        return EntitySelection(self.graph, items)

    def create_grouped_selection(self, groups):
        return GroupedEntities(self.graph, groups)

    def apply(self, func: Callable[[Entity], Any]) -> Any:
        for entity in self.selected_entities:
            func(entity)

    def filter(self, query=None, **query_args):
        raise NotImplementedError()

    def limit(self, limit):
        return self.create_selection(self.selected_entities[:limit])

    def group_by(self, criterion):
        group_criterion_func = None
        if isinstance(criterion, str):
            group_criterion_func = lambda entity: entity.__getattr__(criterion)
        elif callable(criterion):
            group_criterion_func = criterion

        groups = defaultdict(list)

        for entity in self.selected_entities:
            groups[group_criterion_func(entity)].append(entity)

        return self.create_grouped_selection(groups)

    def filter(self, query=None, **query_args):
        return self.create_selection(filter_entities(self.selected_entities, query=query, **query_args))
    
    def intersect(self, other_selection:EntitySelection) -> EntitySelection:
        intersected_entities=[entity for entity in self.get_entities() if entity in other_selection]
        return self.create_selection(intersected_entities)

    def order_by(self, sort_func: Callable[[Entity], Any] = lambda node: node.get_id(), order='asc'):
        reverse = False
        if order == 'desc':
            reverse = True
        return self.create_selection(sorted(self.selected_entities, key=sort_func, reverse=reverse))

    def order_by_desc(self, sort_func: Callable[[Entity], Any]):
        return self.order_by(sort_func, order='desc')

    def order_by_asc(self, sort_func: Callable[[Entity], Any]):
        return self.order_by(sort_func, order='asc')

    def merge(self, other_selection):
        merged_node_selection = [node for node in self.selected_entities]

        for node in other_selection:
            if not node in merged_node_selection:
                merged_node_selection.append(node)

        return self.create_selection(merged_node_selection)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.create_selection(self.selected_entities[item])
        else:
            return self.selected_entities[item]

    def get_property(self,prop) -> List:
        '''
        resolves the given property from each entity in the selection and returns array
        '''
        return [el.get_property(prop) for el in self]

    def get_properties(self,props:list) -> List[List]:
        return list(zip(*[self.get_property(prop) for prop in props]))            

    def __getattr__(self,prop):
        '''
        redirects to get_property()
        '''
        return self.get_property(prop)

    def show_preview(self, n=MAX_PREVIEW_ITEMS):
        print(self._preview_items(n))

    def _preview_items(self, n=MAX_PREVIEW_ITEMS):
        preview_str = "\n"
        for entity in self.selected_entities[:n]:
            preview_str += "- {}\n".format(entity.__repr__())
        if len(self.selected_entities) > n:
            preview_str += "...({} more)".format(len(self.selected_entities) - MAX_PREVIEW_ITEMS)

        return preview_str

    def count(self) -> int:
        return self.__len__()

    def append(self, entity) -> None:
        '''
        appends entity inline
        '''
        self.selected_entities.append(entity)

    def reverse(self) -> EntitySelection:
        return self.create_selection(self.selected_entities[::-1])

    def concat(self, other_selection:EntitySelection) -> None:
        '''
        concats other selection inline
        '''
        for entity in other_selection:
            if entity not in self:
                self.append(entity)
    
    def __contains__(self, entity):
        '''
        TODO: can be done more efficient by using dictionary and accessing only id attribute
        '''
        return entity in self.selected_entities

    def __add__(self, other_collection):
        return self.create_selection(self.selected_entities + other_collection.get_entities())

    def __bool__(self) -> bool:
        return bool(self.selected_entities)

    def __len__(self) -> int:
        return len(self.selected_entities)

    def __repr__(self) -> str:
        return "<Link Selection with {} links>".format(len(self.selected_entities))
