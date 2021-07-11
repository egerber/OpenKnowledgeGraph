class Pattern:
    def __init__(self, node, prop, *args, **kwargs):
        self.node = node
        self.prop = prop

    def matches(self, node, *args, **kwargs):
        pass

    def __hash__(self):
        return hash(())
