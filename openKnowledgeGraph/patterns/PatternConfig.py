from typing import List


class TypeConfig:
    def __init__(self):
        self.config = {"matchers": [], "ignore": []}

    def set_ignore_types(self, types: List[str]):
        self.config["ignore"] = types
        return self

    def set_matchers(self, properties: List[str]):
        self.config["matchers"] = properties
        return self

    def __getitem__(self, item):
        return self.config[item]


class PatternConfig:

    def __init__(self):
        self.config = {"matchers": [], "ignore": []}

    def set_config_for_type(self, type: str, config: TypeConfig):
        self.config[type] = config

    def ignore_types_for_type(self,type:str):
        pass

    def matcher_for_type(self,type:str):
        pass

    def get_child_config(self,name:str):
        return []

    def get_config_for_type(self, type:str) -> TypeConfig:
        return self.config[type]

    def __getitem__(self, item):
        if item in self.config:
            return self.config[item]
        else:
            return TypeConfig()

    @staticmethod
    def for_triplet():
        pattern_config = PatternConfig()

        subject_config = TypeConfig() \
            .set_ignore_types(["relcl", "np", "pp", "postposition"]) \
            .set_matchers(["ner"])

        object_config = TypeConfig() \
            .set_ignore_types(["relcl"]) \
            .set_matchers(["ner"])

        pattern_config.set_config_for_type("subject", subject_config)
        pattern_config.set_config_for_type("object", object_config)

        return pattern_config

    @staticmethod
    def for_constituent_tree(max_depth=10):
        pass

    @staticmethod
    def for_dependency_tree(max_depth=20):
        pass
