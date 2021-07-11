# Open-Knowledge-Graph

## Introduction
<code>OpenKnowledgeGraph</code> is a allows to represent texts as a graphs and allows to work with entities in a structured manner. Among other it has the following features
* Split up Conjugational Sentences into simple parts
* Sentence Canonicalization (<i>"Thomas likes to play piano and go skiing"</i> => [<i>"Thomas likes to play piano"</i>, <i>"Thomas likes to go skiing"</i>])
* extract entities from the text and link coreferences (using neuralcoref package)
* constituency graph (generated from the spacy dependency parse tree)
* find statistical frequent expressions in the text (e.g. "[NP] shows that [VP])
* extract knowledge triplets from text
* save graph to disk and reload
* search for entities across multiple documents
* creating new nodes, adding custom properties, and connecting nodes
* creating pipeline for processing texts

## Examples

```python
from openKnowledgeGraph import OpenKnowledgeGryph

sample_text="Thomas likes to go skiing and play the guitar"
g=OpenKnowledgeGraph.from_text(sample_text)

g.find_nodes(Q(type="np"))
'''

'''

g.find_nodes(Q(type="token",pos="noun")
'''

'''
```

## Nodes and Links
The Graph contains two types of entities: Nodes and Links. Nodes allow to store properties about an entity, as well as define custom computed properties. Links connect two Nodes.
Both nodes and links have the following attributes:
* type (e.g. token, dependency, np, vp, ...or anything custom)
* attributes (key-value dictionary)

### Nodes
* <code>TokenNode</code>
* <code>ConstituentNode</code>
* <code>NerNode</code>
* <code>ReferenceNode</code>
* <code>DecoratorNode</code>


### Links

## Query
Queries allow to search for nodes and links using:
* <code>graph.find_nodes(Q(...))</code> (short: <code>graph.fn(Q(...)))</code>)
* <code>graph.find_links(Q(...))</code> (short: <code>graph.fl(Q(...)))</code>)

* <code>filter</code>
* <code>group_by</code>
* <code>order_by(sort_func,order='asc')</code>
* <code>order_by_desc(sort_func)</code>
* <code>order_by_asc(sort_func)</code>
* <code>merge(other_selection: EntitySelection)</code>
* <code>append(element)</code>
* <code>show_preview()</code>


### Q
<code>Q</code>

### EntitySelection
<code>NodeSelection</code> and <code>LinkSelection</code> derive from <code>EntitySelection</code> and have the following attributes:


### GroupedEntities
<code>GroupedEntities</code>

## Operations
### ConstituentTransformer

### CanonicalizationTransformer


