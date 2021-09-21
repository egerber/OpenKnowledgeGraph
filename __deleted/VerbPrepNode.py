from openKnowledgeGraph.nodes.Node import Node


class VerbPrepNode(Node):

    def __init__(self, vp, pp,**kwargs):
        Node.__init__(self,**kwargs)
        self.vp = vp
        self.pp = pp

    def get_id(self):
        return hash(("verb_prep", self.vp.get_id(), self.pp.get_id()))

    @staticmethod
    def get_type():
        return "verb_prep"

    def get_text(self):
        return "({}, {})".format(self.vp.text, self.pp.text)
