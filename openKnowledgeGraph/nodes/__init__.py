from openKnowledgeGraph.nodes.CanonicalNode import CanonicalNode
from .TokenNode import TokenNode
from .NoneNode import NoneNode
from .classifications.NerNode import NerNode
from .constituents import AdjpNode, AdvclNode, AdvpNode, \
    ConstituentNode,  NPNode, PPNode, SbarNode, VPNode
from .NodeRegistry import NodeRegistry
from .CanonicalVPNode import CanonicalVPNode
from openKnowledgeGraph.nodes.ConstituentNode2 import ConstituentNode2


all_node_types = [
    TokenNode,
    NoneNode,
    NerNode, AdjpNode, AdvclNode, AdvpNode,
    ConstituentNode, NPNode, PPNode, SbarNode, VPNode, CanonicalVPNode,
    ConstituentNode2,
    CanonicalNode
]

for node_type in all_node_types:
    NodeRegistry.register_node(node_type.name, node_type)

__all__ = all_node_types + [NodeRegistry]
