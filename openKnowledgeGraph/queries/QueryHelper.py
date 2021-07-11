from openKnowledgeGraph.queries.QuerySet import Q, QNode


def filter_entities(entities, *queries, **query_args):
    '''
    #TODO pass indices in here as well to add performance optimization
    :param entities:
    :param queries:
    :param query_args:
    :return:
    '''
    if len(queries) == 0:
        query_args = {key: value for key, value in query_args.items() if not key == "entities"}
        query = Q(**query_args)
        return query(entities)
    elif len(queries) >= 1 and isinstance(queries[0], QNode) and (len(queries) > 1 or len(query_args) > 0):
        raise ValueError(
            "Only one query element Q(x=y) can be processed. If you want to combine multiple filters, connect your queries using '&' and '|' operator")
    elif all([isinstance(arg, QNode) for arg in queries]):
        return queries[0](entities)
    else:
        raise ValueError("Arguments {}, {} are not valid".format(queries, query_args))
