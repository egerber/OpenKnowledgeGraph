class LinkRegistry:
    LinkTypes = {}

    @staticmethod
    def register_link(type, LinkClass):
        LinkRegistry.LinkTypes[type] = LinkClass

    @staticmethod
    def get_by_type(link_type):
        if link_type in LinkRegistry.LinkTypes:
            return LinkRegistry.LinkTypes[link_type]
        else:
            return None