from openKnowledgeGraph import OpenKnowledgeGraph
from openKnowledgeGraph.queries import Q

sample_text="Thomas likes to go skiing and play the guitar"
g=OpenKnowledgeGraph.from_text(sample_text)

print(g.find_nodes(Q(type="np")))