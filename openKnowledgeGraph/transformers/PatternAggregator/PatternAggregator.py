from collections import defaultdict

from openKnowledgeGraph.hierarchicalPatterns.HierarchicalPattern import HierarchicalPattern
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.statistics.AggregatedPatterns import AggregatedPatterns
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
import collections


class PatternAggregator(GraphOperation):

    def __init__(self, config, *args, **kwargs):
        GraphOperation.__init__(self, *args, **kwargs)

        self.config = config
        self.pattern_counter = collections.Counter()
        self.instances_by_pattern = defaultdict(list)

    def get_pattern(self):
        return Q(type="vp")

    def apply(self, node, *args, **kwargs):
        pattern = HierarchicalPattern(node, config=self.config)

        self.instances_by_pattern[pattern].append(node)
        self.pattern_counter.update([pattern])

    def after_apply(self, nodes, returned_values, *args, **kwargs):
        return AggregatedPatterns(self.pattern_counter, self.instances_by_pattern)
