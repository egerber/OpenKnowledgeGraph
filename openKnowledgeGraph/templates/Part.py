class Part:
    def __init__(self, value):
        self.value = value

    def get_text(self):
        return self.value

    def is_atomic(self):
        return True

    def get_arguments(self):
        return []

    def get_nested_arguments(self):
        return []

    def get_property(self, name: str) -> any:
        return self.get_value().__getattr__(name)

    @property
    def dof(self):
        return self.get_dof()

    def get_dof(self):
        '''
        degrees of freedom (how many parameters/arguments can be modified)
        :return:
        '''
        return 0

    def get_value(self):
        return self.value

    def __hash__(self):
        return hash((self.get_value()))

    def to_text(self):
        return self.value

    def __repr__(self):
        return "<Part {}>".format(self.to_text())

    def get_identifier(self):
        return "{}".format(self.get_value())

    def __len__(self):
        '''
        returns of how many (sub) parts this part is composed of
        :return:
        '''
        return 1

    @staticmethod
    def get_type():
        return "default"

    @property
    def preview(self):
        pass

    def to_pattern(self,pattern_config,current_depth_by_type={}):
        raise NotImplementedError()
