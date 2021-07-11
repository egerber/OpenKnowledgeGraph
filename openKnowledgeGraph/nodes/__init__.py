from .TokenNode import TokenNode
from .DependencyNode import DependencyNode
from .DecoratorNode import DecoratorNode
from .NoneNode import NoneNode
from .ReferenceNode import ReferenceNode
from .SpanNode import SpanNode
from .UndefinedConstituencyNode import UndefinedConstituencyNode
from .VerbPrepNode import VerbPrepNode
from .classifications.NerNode import NerNode
from .classifications.PPTypeNode import PPTypeNode
from .constituents import AdjpNode, AdvclNode, AdvpNode, \
    ConstituentNode, ListNode, NPNode, PPNode, SbarNode, VPNode
from .NodeRegistry import NodeRegistry
from .CanonicalVPNode import CanonicalVPNode

all_node_types = [
    TokenNode,
    DependencyNode,
    DecoratorNode,
    NoneNode,
    ReferenceNode,
    SpanNode, UndefinedConstituencyNode, VerbPrepNode, NerNode, PPTypeNode, AdjpNode, AdvclNode, AdvpNode,
    ConstituentNode, ListNode, NPNode, PPNode, SbarNode, VPNode, CanonicalVPNode
]

for node_type in all_node_types:
    NodeRegistry.register_node(node_type.get_type(), node_type)

__all__ = all_node_types + [NodeRegistry]
