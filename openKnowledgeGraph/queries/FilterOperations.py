def filter_entities_by_custom_filter(nodes, filter_func=lambda node: True):
    return list(filter(filter_func, nodes))


def filter_entities_by_attribute(entities, key, value):
    return [entity for entity in entities if entity.__getattr__(key) == value]


def filter_entities_by_property(entities, property, value):
    '''
        :param entities:
        :param key:

        POSTFIXES: (compare to here: https://docs.mongoengine.org/guide/querying.html)
        __in
        __nin
        __not
        __exact (string)
        __contains (string)

        optional (could implement later):
        __lt
        __lte (less than equal)
        __gt
        __gte
        __size (for array)

        :param value:

        example type__nin=['triplet', 'independent_clause']
        :return:
    '''
    if property.endswith('__in'):
        return [entity for entity in entities if entity.__getattr__(property[:-4]) in value]
    elif property.endswith('__nin'):
        return [entity for entity in entities if not entity.__getattr__(property[:-5]) in value]
    elif property.endswith('__not'):
        return [entity for entity in entities if not entity.__getattr__(property[:-5]) == value]
    elif property.endswith('__contains'):
        attribute_key = property[:-10]
        filtered_elements = []
        for entity in entities:
            property_value = entity.get_property(attribute_key)
            if property_value and value in property_value:
                filtered_elements.append(entity)

        return filtered_elements
    else:
        return [entity for entity in entities if entity.get_property(property) == value]


def filter_entities_by_single_filter(entities, key, value):
    if key == 'custom':
        return filter_entities_by_custom_filter(entities, value)
    else:
        return filter_entities_by_property(entities, key, value)
