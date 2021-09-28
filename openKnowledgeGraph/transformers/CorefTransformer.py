from __future__ import annotations
import os
from typing import TYPE_CHECKING
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.queries.QuerySet import Q
from spacy.tokens import Doc

if TYPE_CHECKING:
    from openKnowledgeGraph.OpenKnowledgeGraph import OpenKnowledgeGraph


class CorefTransformer:
    '''
    links coreferences
    '''

    def __call__(self, graph:OpenKnowledgeGraph, doc:Doc, *args, **kwargs):
        successful_coref_resolutions = 0
        failed_coref_resolutions = 0
        for coref_cluster in doc._.coref_clusters:
            main_cluster = coref_cluster.main

            # ensure that cluster [Paul McCartney] is not matched with [Paul McCartney and his wife] by matching the full_text of the np with the span from the cluster
            main_np_candidates = main_cluster.root._.token_node.find_in_nodes(type="constituent",constituent_type="np")

            if len(main_np_candidates)>1:
                print("ERROR: multiple candiates for coref of '{}' possible. Taking first".format(main_cluster.root._.token_node.text))

            main_np=main_np_candidates.first()
            if main_np is not None:
                for reference in coref_cluster:
                    if reference == main_cluster:
                        continue
                    reference_np = doc[reference.root.i]._.token_node.find_in_nodes(type="constituent",constituent_type="np").first()

                    if reference_np is None:
                        if os.environ.get('DEBUG'):
                            print("reference_np is None: '{} (index {})' ".format(reference, reference[0].i))
                        failed_coref_resolutions += 1
                    else:
                        graph.create_link("coref", source=reference_np, target=main_np)
                        successful_coref_resolutions += 1
        
        if os.environ.get('DEBUG'):
            print("successful coref resolutions: {}".format(successful_coref_resolutions))
            print("failed ner coref: {}".format(failed_coref_resolutions))
        
        graph.register_component("coref")