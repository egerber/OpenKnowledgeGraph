from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.transformers.ConstituentTransformers.AdjpTransformer import \
    AdjpTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.AdvclTransformer import \
    AdvclTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.AdvpTransformer import \
    AdvpTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.NPTransformer import NPTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.PPTransformer import PPTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.SbarTransformer import \
    SbarTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.VPTransformer import VPTransformer


class ConstituentTransformer2(GraphOperation):
    
    def __init__(self, **kwargs):
        GraphOperation.__init__(self, **kwargs)
    

    def apply(self, node:Node, *args, **kwargs):

        constituent_type="unknown"
        if node.matches(Q(dep="advcl")):
            constituent_type="advcl" #advcl
        elif node.matches(Q(dep="ccomp")):
            constituent_type="sbar" #sbar
        elif node.matches(Q(dep__in=["nsubj", "nsubjpass", "pobj", "dobj", "poss"]) | 
            Q(pos__in=["noun", "propn", "pron"])):
            constituent_type="np" #NP
        elif node.matches(Q(dep__in=["prep", "agent"])):
            constituent_type="pp" #PP
        elif node.matches(Q(dep="acomp") | Q(pos="adj")):
            constituent_type="advp" #advp
        elif node.matches(Q(type="dependency", dep__in=["root", "ccomp", "relcl", "xcomp", "advcl"]) | 
                                                                                        Q(pos="verb") | 
                                                                                        Q(pos="aux",lemma="be")):
            constituent_type="vp"
        elif node.matches(Q(dep="acomp") | Q(pos="adj")):
            constituent_type="adjp" #adjp
        else:
            print("no logic for node",node)

        constituent=node.get_graph().create_reference_node(
            reference_node=node,node_type="constituent2",
            properties={'constituent_type':constituent_type}
        )
       
        for token in node.find_out_links(type="dependency").target_nodes:
            child_constituent=self.apply(token,*args,**kwargs)
            node.get_graph().create_link(
                link_type="constituent",
                source=constituent, 
                target=child_constituent,
                dep=child_constituent.dep
            )
        
        return constituent

    @staticmethod
    def get_name():
        return "constituent2"

    def get_pattern(self):
        return Q(type="token", dep="root")
