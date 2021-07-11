from openKnowledgeGraph.hierarchicalPatterns.Pattern import Pattern


class HierarchicalPattern:

    def __init__(self, node, config, *args, **kwargs):
        self.config = config
        self.node_property = config['node_property']
        max_depth = config['max_depth']

        if self.node_property is not '?':
            self.value = node.__getattr__(self.node_property)
        else:
            self.value = '[]'

        self.left_children = []
        self.right_children = []
        if max_depth is None or max_depth > 0:
            for child in node.left_children:
                if not self.is_child_ignored(child):
                    self.left_children.append(self.create_sub_pattern_for_child(child))
            for child in node.right_children:
                if not self.is_child_ignored(child):
                    self.right_children.append(self.create_sub_pattern_for_child(child))

    def create_sub_pattern_for_child(self, child):
        props_for_child = self.get_props_for_child(child)
        '''
        TODO decrement max_depth'''
        if 'max_depth' in props_for_child and props_for_child['max_depth'] is not None:
            props_for_child['max_depth'] -= 1
        return HierarchicalPattern(child, config=props_for_child)

    @staticmethod
    def merge_properties(special_properties, base_properties):
        '''
        TODO: check if properties_by_type should also be inherited
        :param special_properties:
        :param base_properties:
        :return:
        '''
        merged_properties = {}
        for key, value in special_properties.items():
            if key == 'by_type':
                continue
            merged_properties[key] = value

        for key, value in base_properties.items():
            if key == 'by_type':
                continue
            elif key not in merged_properties:
                merged_properties[key] = value

        if 'by_type' in special_properties:
            merged_properties['by_type'] = HierarchicalPattern.merge_properties(special_properties['by_type'],
                                                                                base_properties['by_type'])

        return merged_properties

    def get_config_by_type(self, child):
        if 'by_type' not in self.config:
            return None
        config_by_type = self.config['by_type']
        if child.type in config_by_type:
            return config_by_type[child.type]
        elif '*' in config_by_type:
            '''matches for all types'''
            return config_by_type['*']
        else:
            return None

    def is_child_ignored(self, child):
        if 'ignore_types' in self.config:
            if self.config['ignore_types'] == '*':
                '''
                if type is specified explicitly, dont use ignore *'''
                return self.get_config_by_type(child) is None
            else:
                return child.get_type() in self.config['ignore_types']

        return False

    def get_props_for_child(self, child):
        config_for_child = self.get_config_by_type(child)
        if config_for_child:
            return self.merge_properties(config_for_child, self.config)
        else:
            return self.merge_properties({}, self.config)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def to_string(self):
        self_str = f'{self.value}'

        left_children_str = ' '.join([child.to_string() for child in self.left_children])
        right_children_str = ' '.join([child.to_string() for child in self.right_children])

        if len(self.left_children) == 0 and len(self.right_children) == 0:
            return self_str
        elif len(self.left_children) > 0 and len(self.right_children) == 0:
            return f'{left_children_str} {self_str}'
        elif len(self.right_children) > 0 and len(self.left_children) == 0:
            return f'{self_str} {right_children_str}'
        else:
            return f'{left_children_str} {self_str} {right_children_str}'

    @staticmethod
    def get_type():
        return "HierarchicalPattern"

    def __repr__(self):
        return f'<{self.get_type()} :{self.to_string()}>'

    def __hash__(self):
        left_children_tuple = tuple(self.left_children)
        right_children_tuple = tuple(self.right_children)
        root = self.value

        return hash((root, left_children_tuple, right_children_tuple))

    def to_template(self, instance):
        pass
