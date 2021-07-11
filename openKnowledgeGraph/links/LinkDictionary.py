from collections import defaultdict

DEBUG = True


class LinkDictionary:

    def __init__(self):
        self.links_by_id = {}

        self.inlinks_by_node_id = defaultdict(list)
        self.outlinks_by_node_id = defaultdict(list)

    def add(self, link, override_if_exists=False):
        link_exists = link.get_id() in self.links_by_id

        if link_exists and DEBUG:
            print("WARNING: link_id {} ({}) is already registered in LinkDictionary".format(link.get_id(), link))

        if not link_exists or override_if_exists:
            self.links_by_id[link.get_id()] = link
            self.inlinks_by_node_id[link.get_target_id()].append(link)
            self.outlinks_by_node_id[link.get_source_id()].append(link)

    def __getitem__(self, item):
        return self.links_by_id[item]

    def __contains__(self, item):
        return item in self.links_by_id

    def __len__(self):
        return len(self.links_by_id)

    def get_inlinks_for_node(self, node):
        return self.inlinks_by_node_id[node.get_id()]

    def get_links_for_node(self, node):
        return self.inlinks_by_node_id[node.get_id()] + self.outlinks_by_node_id[node.get_id()]

    def get_links(self):
        return list(self.links_by_id.values())

    def get_outlinks_for_node(self, node):
        return self.outlinks_by_node_id[node.get_id()]

    def remove(self, link) -> None:
        link_id = link.get_id()
        link = self.links_by_id[link_id]
        if link is None:
            return

        source_id = link.get_source_id()
        target_id = link.get_target_id()

        self.outlinks_by_node_id[source_id].remove(link)
        self.inlinks_by_node_id[target_id].remove(link)

        del self.links_by_id[link_id]

    @staticmethod
    def create_from_links(links):
        link_dictionary = LinkDictionary()
        for link in links:
            link_dictionary.add(link)

        return link_dictionary
