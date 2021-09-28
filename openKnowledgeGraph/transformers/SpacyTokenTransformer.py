from __future__ import annotations
from typing import TYPE_CHECKING
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.highlevel.IndependentClauseNode import IndependentClauseNode
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.queries.QuerySet import Q
from openKnowledgeGraph.nodes.TokenNode import TokenNode
from spacy.tokens import Token
from spacy.tokens import Doc

if TYPE_CHECKING:
    from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class SpacyTokenTransformer:
    '''
    imports tokens from spacy doc into graph
    # TODO technically not a transformer -> create new base class for input based transformation
    '''

    def __call__(self, graph:OpenKnowledgeGraph, doc:Doc, *args, **kwargs):
        Token.set_extension("token_node", default=None, force=True)
        last_sent_node = None
        graph.create_node(node_type="document",properties={'text':doc.text})
        for _, sent in enumerate(doc.sents):
            current_sent_node = graph.create_node(node_type="sentence",properties={'text':sent.text})
            if last_sent_node is not None:
                graph.create_link("temporal", last_sent_node, current_sent_node)

            for token in sent:
                token_node = graph.create_node(node_type="token", properties={
                    "text": token.text,
                    "lemma": token.lemma_,
                    "i": token.i,
                    "pos": token.pos_.lower(),
                    "tag": token.tag_.lower(),
                    "dep": token.dep_.lower(),
                    "whitespace": token.whitespace_
                })
                
                doc[token.i]._.token_node = token_node

            root_node = sent.root._.token_node
            graph.create_link("dependency", current_sent_node, root_node, dependency_type="root")

            for token in sent:
                for child in token.children:
                    graph.create_link("dependency", 
                        token._.token_node, 
                        child._.token_node,
                        dependency_type=child.dep_)

            last_sent_node = current_sent_node

        graph.register_component("token")