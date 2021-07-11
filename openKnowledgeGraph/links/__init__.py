from openKnowledgeGraph.links.AdvclLink import AdvclLink
from openKnowledgeGraph.links.ArgumentLink import ArgumentLink
from openKnowledgeGraph.links.BroadcastLink import BroadcastLink
from openKnowledgeGraph.links.CorefLink import CorefLink
from openKnowledgeGraph.links.DecoratorLink import DecoratorLink
from openKnowledgeGraph.links.DependencyLink import DependencyLink
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry
from openKnowledgeGraph.links.ParentLink import ParentLink
from openKnowledgeGraph.links.ReferenceLink import ReferenceLink
from openKnowledgeGraph.links.TemporalLink import TemporalLink

all_link_types = [ReferenceLink, ParentLink, TemporalLink, CorefLink, DependencyLink, BroadcastLink, ArgumentLink,
                  AdvclLink,
                  DecoratorLink]

for link_type in all_link_types:
    LinkRegistry.register_link(link_type.get_type(), link_type)
