from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.relations.RelationNode import RelationNode


class InstanceOfRelation(RelationNode):
    def __init__(self, **kwargs):
        RelationNode.__init__(self, **kwargs)

    def get_entity(self):
        return self.find_argument("entity")

    def get_group(self):
        return self.find_argument("group")

    @staticmethod
    def get_type():
        return "rel_instance_of"

    @staticmethod
    def from_arguments(entity, group):
        graph = entity.get_graph()
        instance_of_node = InstanceOfRelation()

        graph.add_node(instance_of_node)

        links = [Link.create("argument", instance_of_node, entity, argument_type="entity"),
                 Link.create("argument", instance_of_node, group, argument_type="group")]
        graph.add_links(links)

        return instance_of_node
