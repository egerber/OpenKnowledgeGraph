from openKnowledgeGraph.links.LinkRegistry import LinkRegistry

all_link_types = []

for link_type in all_link_types:
    LinkRegistry.register_link(link_type.get_type(), link_type)
