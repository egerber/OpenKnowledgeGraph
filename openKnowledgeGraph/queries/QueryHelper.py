from __future__ import annotations
from typing import TYPE_CHECKING, List
from openKnowledgeGraph.queries.QuerySet import Q, QNode

if TYPE_CHECKING:
    from openKnowledgeGraph.Entity import Entity

def filter_entities(entities, query:Q=None, **query_args) -> List[Entity]:
    '''
    #TODO pass indices in here as well to add performance optimization
    :param entities:
    :param queries:
    :param query_args:
    :return:
    '''
    if query is None:
        query_args = {key: value for key, value in query_args.items() if not key == "entities"}
        query = Q(**query_args)
        return query(entities)
    elif query:
        return query(entities)
    elif query is None and len(query_args.keys())==0:
        #no filter logic given -> return all entities
        return entities
    else:
        raise ValueError("Arguments {}, {} are not valid".format(query, query_args))
