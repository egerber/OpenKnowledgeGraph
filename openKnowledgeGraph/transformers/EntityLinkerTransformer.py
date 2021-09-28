from __future__ import annotations
from typing import TYPE_CHECKING
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q
from spacy.tokens import Doc

if TYPE_CHECKING:
    from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class EntityLinkerTransformer:
    '''
    connects information about entities to np constituents
    '''

    def __call__(self, graph:OpenKnowledgeGraph, doc:Doc, *args, **kwargs):
        for linked_entity in doc._.linkedEntities:
            entity_span = linked_entity.get_span()

            main_np_candidates = entity_span.root._.token_node.find_in_nodes(type="constituent", constituent_type="np")
            if len(main_np_candidates)>1:
                print("ERROR: multiple candiates for '{}' possible. Taking first".format(entity_span))
            
            main_np=main_np_candidates.first()
            if main_np is not None:
                graph.create_decorator_node(source_node=main_np, node_type="linked_entity",
                                           properties={'entity_id':linked_entity.get_id(),
                                                    'entity_label':linked_entity.get_label()})

        graph.register_component("entity_linker")
        