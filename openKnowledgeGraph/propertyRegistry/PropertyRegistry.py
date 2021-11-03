from collections import defaultdict

class PropertyRegistry:

    def __init__(self):
        self.properties_by_id=defaultdict(dict)
        self.computed_properties_by_id=defaultdict(dict)
        self.nested_properties_by_id=defaultdict(dict)

    def get_properties_for_id(self,id:str):
        return self.properties_by_id[id]
    
    def get_property_for_id(self,id:str,key:str):
        if key in self.properties_by_id[id]:
            return self.properties_by_id[id][key]
        else:
            return None

    def get_nested_property_for_id(self, id:str, key:str):
        if key in self.nested_properties_by_id[id]:
            return self.nested_properties_by_id[id][key]
        else:
            return None        
    
    def get_properties_for_id(self, id:str):
        #
        return {prop:value for prop,value in self.properties_by_id[id].items() if prop not in ["source_id","target_id","graph","type","id"]}

    def set_properties_for_id(self,id:str, **properties):
        self.properties_by_id[id]=properties
    
    def set_property_for_id(self,id:str,key:str,value:str):
        self.properties_by_id[id][key]=value

    def set_nested_property_for_id(self, id:str, key:str, value:str):
        self.nested_properties_by_id[id][key]=value

    def register_computed_property_for_id(self, id:str, key:str):
        self.computed_properties_by_id[id][key]=-1

    def has_property(self,id:str,key:str):
        return key in self.properties_by_id[id]

    def has_computed_property(self,id:str,key:str):
        return  key in self.computed_properties_by_id[id]

    def has_nested_property(self, id:str, key:str):
        return key in self.nested_properties_by_id[id]