import bz2
import pickle
import string
from collections import defaultdict
import _pickle as cPickle
import logging

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from spacy.tokens import Token

from openKnowledgeGraph.nodes.highlevel.DocumentNode import DocumentNode
from openKnowledgeGraph.nodes import DecoratorNode
from openKnowledgeGraph.nodes import NodeRegistry
from openKnowledgeGraph.index.Index import Index
from openKnowledgeGraph.links.LinkDictionary import LinkDictionary
from openKnowledgeGraph.links.CorefLink import CorefLink
from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.nodes.highlevel.SentenceNode import SentenceNode
from openKnowledgeGraph.selections.KnowledgeGraphSubset import KnowledgeGraphSubset
from openKnowledgeGraph.selections.LinkSelection import LinkSelection
from openKnowledgeGraph.selections.NodeSelection import NodeSelection
from openKnowledgeGraph.nodes.TokenNode import TokenNode
from openKnowledgeGraph.queries.QueryHelper import filter_entities
from openKnowledgeGraph.transformers.Classification.PPTypeTransformer import PPTypeTransformer
from openKnowledgeGraph.transformers.ConstituentTransformers.ConstituentTransformer import \
    ConstituentTransformer
from openKnowledgeGraph.transformers.GraphOperation import GraphOperation
from openKnowledgeGraph.transformers.IndependentClauseTransformer import \
    IndependentClauseTransformer
from spacyEntityLinker import EntityLinker

import random
import neuralcoref
import spacy

DEBUG = False
PREFIX_LENGTH = 10

PRE_LOADED_PIPELINES_BY_MODEL = {

}


class OpenKnowledgeGraph:

    def __init__(self, nodes_by_id=None, link_dictionary=None, index_to_ids=None):
        if index_to_ids is None:
            index_to_ids = defaultdict(list)
        if link_dictionary is None:
            link_dictionary = LinkDictionary()
        if nodes_by_id is None:
            nodes_by_id = dict()

        self._doc = None  # TODO remove later: only for debugging

        self.properties_by_node_id = {}

        self.index_by_type = Index("type")

        self.nodes_by_id = nodes_by_id
        self.link_dictionary = link_dictionary

        self.index_to_ids = index_to_ids

        self.id_counter = 0

        self.init_id_prefix(''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(PREFIX_LENGTH)))

    def init_id_prefix(self, prefix):
        '''
        allows to specify unique prefix in order to avoid id collisions between distinct graphs
        this is important when different graphs of different documents are "merged"
        :param prefix:
        :return:
        '''
        self.id_prefix = prefix

    def generate_new_id(self):
        id = self.id_counter
        self.id_counter += 1

        return "{}_{}".format(self.id_prefix, id)

    def add_link(self, link, override_if_exists=False, assign_id=True):
        link.set_graph(self)
        if assign_id:
            link.set_id(self.generate_new_id())
        self.link_dictionary.add(link, override_if_exists=override_if_exists)

    def add_links(self, links, override_if_exists=False):
        for link in links:
            self.add_link(link, override_if_exists=override_if_exists)

    def remove_link(self, link):
        self.link_dictionary.remove(link)

    def get_inlinks_for_node(self, node, *queries, **query_args):
        return filter_entities(self.link_dictionary.get_inlinks_for_node(node), *queries, **query_args)

    def get_outlinks_for_node(self, node, *queries, **query_args):
        return filter_entities(self.link_dictionary.get_outlinks_for_node(node), *queries, **query_args)

    def get_links_for_node(self, node, *queries, **query_args):
        return filter_entities(self.link_dictionary.get_links_for_node(node), *queries, **query_args)

    def get_node(self, node_id):
        return self.nodes_by_id[node_id]

    def get_link(self, link_id):
        return self.link_dictionary[link_id]

    def add_node(self, node, override_if_exists=False, assign_id=True):
        node_exists = node.get_id() in self.nodes_by_id
        if node_exists and DEBUG:
            print("WARNING: node id already in graph: ", node)

        if not node_exists or override_if_exists:
            if assign_id:
                node.set_id(self.generate_new_id())
            self.nodes_by_id[node.get_id()] = node
            # self.indices += node.get_indices()
            node.set_graph(self)
        if not node_exists:
            self.index_by_type.add_entry(node.get_type(), node)

    def get_links_for_nodes(self, nodes):
        return [link for link in self.link_dictionary.get_links() if
                link.get_source() in nodes or link.get_target() in nodes]

    def get_nodes(self):
        return list(self.nodes_by_id.values())

    def draw_node_connections(self, scale_factor=1., save=False, filter_nodes=lambda node: True,
                              filter_entities=lambda link: True):
        DISTANCE_FACTOR = 3.
        MIN_NODE_SIZE = 1000
        MAX_NODE_SIZE = 2000

        NODE_COLORS_BY_TYPE = defaultdict(lambda: "grey", {
            "triplet": "red",
            "complex_triplet": "red",
            "object": "blue",
            "coref": "#dddddd",
            "list": "#dddddd",
            "subject_tuple": "yellow",
            "object_tuple": "yellow",
            "attribute": "green"
        })

        EDGE_COLORS_BY_TYPE = defaultdict(lambda: "grey", {
            "preposition": "green",
            "argument": "red",
            "broadcast": "blue",
            "object_preposition": "green",
        })

        EDGE_WIDTHS_BY_TYPE = defaultdict(lambda: 1, {
            "preposition": 2,
            "argument": 5,
            "broadcast": 1,
            "object_preposition": 2
        })

        edge_list = [(link.get_source_id(), link.get_target_id()) for link in self.link_dictionary.get_links() if
                     filter_entities(link)]

        G = nx.Graph()
        for node in self.get_nodes():
            G.add_node(node.get_id())

        G.add_edges_from(edge_list)

        count_inlinks_by_node = []
        for node_id in G.nodes:
            if node_id in self.nodes_by_id:
                count_inlinks_by_node.append(len(self.get_node(node_id).get_inlinks_for_node()))
            else:
                count_inlinks_by_node.append(1)

        min_count_inlinks = min(count_inlinks_by_node)
        max_count_inlinks = max(count_inlinks_by_node)
        node_sizes = []
        labeldict = defaultdict(lambda: 'undefined')
        for node_id in G.nodes:

            if node_id in self.nodes_by_id:
                count_inlinks = len(self.get_node(node_id).get_inlinks_for_node())
                node_sizes.append(MIN_NODE_SIZE + MAX_NODE_SIZE * (count_inlinks / (1 + max_count_inlinks)) / (
                        (min_count_inlinks + 1) / (1 + max_count_inlinks)))
                labeldict[node_id] = self.nodes_by_id[node_id].get_text()
            else:
                node_sizes.append(MIN_NODE_SIZE)
                labeldict[node_id] = "undefined"

        color_map_nodes = []
        for node_id in G:
            if node_id in self.nodes_by_id:
                color_map_nodes.append(NODE_COLORS_BY_TYPE[self.nodes_by_id[node_id].get_type])
            else:
                color_map_nodes.append('grey')

        color_map_edges = []
        width_map_edges = []
        for link in self.link_dictionary.get_links():
            color_map_edges.append(EDGE_COLORS_BY_TYPE[link.get_type])
            width_map_edges.append(EDGE_WIDTHS_BY_TYPE[link.get_type])

        plt.figure(0, figsize=(22 * scale_factor, 22 * scale_factor))

        pos = nx.spring_layout(G, k=DISTANCE_FACTOR / np.sqrt(len(G.nodes())))
        # pos = nx.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=color_map_nodes)
        nx.draw_networkx_labels(G, pos, labels=labeldict)
        nx.draw_networkx_edges(G, pos, arrows=True, edge_color=color_map_edges, width=width_map_edges,
                               connectionstyle="arc3,rad=0.2")

        if not save:
            plt.show(block=False)
        else:
            plt.savefig("Graph.png", format="PNG")

    def get_links(self, *queries, **query_args):
        return filter_entities(self.link_dictionary.get_links(), *queries, **query_args)

    def resolve_coreferences(self):
        coref_links = [link for link in self.get_links() if isinstance(link, CorefLink)]

        for coref_link in coref_links:
            for inlink in coref_link.get_source().get_inlinks_for_node():
                self.add_link(inlink.clone_with_properties(inlink.get_source_id(), coref_link.get_target_id()))
                self.remove_link(inlink)
            self.remove_link(coref_link)

    def filter_by_links(self, *queries, **query_args):
        link_selection = filter_entities(self.get_links(), *queries, **query_args)

        return self.subselection_from_links(link_selection)

    def filter_by_nodes(self, *queries, **query_args):
        node_selection = filter_entities(self.get_nodes(), *queries, **query_args)
        return self.subselection_from_nodes(node_selection)

    def subselection_from_links(self, link_selection):
        filtered_nodes_by_id = {}
        for link in link_selection:
            filtered_nodes_by_id[link.get_source_id()] = link.get_source()
            filtered_nodes_by_id[link.get_target_id()] = link.get_target()

        return KnowledgeGraphSubset(self,
                                    nodes_by_id=filtered_nodes_by_id,
                                    link_dictionary=LinkDictionary.create_from_links(link_selection))

    def subselection_from_nodes(self, node_selection):
        filtered_links = self.get_links_for_nodes(node_selection)

        return KnowledgeGraphSubset(self,
                                    nodes_by_id={node.get_id(): node for node in node_selection},
                                    link_dictionary=LinkDictionary.create_from_links(filtered_links))

    def create_link(self, link_type, source, target, **kwargs):
        new_link = Link.create(link_type, source, target, **kwargs)
        self.add_link(new_link)

        return new_link

    def create_node(self, node_type, properties=None):
        if properties is None:
            properties = {}
        NodeClass = NodeRegistry.get_by_type(node_type)

        if NodeClass is not None:
            new_node = NodeClass(**properties)
        else:
            from openKnowledgeGraph.nodes.CustomNode import CustomNode
            new_node = CustomNode(node_type, **properties)

        self.add_node(new_node)

        self.properties_by_node_id[new_node.get_id()] = properties

        return new_node

    def create_decorator_node(self, source_node, node_type, **kwargs):
        NodeClass = NodeRegistry.get_by_type(node_type)

        if NodeClass is not None:
            decorator_node = NodeClass(**kwargs)
        else:
            from openKnowledgeGraph.nodes.CustomDecoratorNode import CustomDecoratorNode
            decorator_node = CustomDecoratorNode(node_type, **kwargs)
        self.add_node(decorator_node)

        DecoratorNode.create_decorator_link(decorator_node, source_node)
        self.properties_by_node_id[decorator_node.get_id()] = kwargs

        return decorator_node

    def create_reference_node(self, reference_node, node_type, **kwargs):
        new_node = self.create_node(node_type, **kwargs)
        self.create_link(link_type="reference", source=new_node, target=reference_node)

        return new_node

    def process_dependency_nodes(self, doc):
        Token.set_extension("token_node", default=None, force=True)
        last_sent_node = None
        self.add_node(DocumentNode.from_spacy_doc(self,doc))
        for index, sent in enumerate(doc.sents):
            current_sent_node = SentenceNode.from_spacy_sent(self, sent)
            if last_sent_node is not None:
                self.add_link(Link.create("temporal", last_sent_node, current_sent_node))

            for token in sent:
                token_node = TokenNode.from_spacy_token(self, token)
                doc[token.i]._.token_node = token_node

            root_node = sent.root._.token_node
            self.add_link(Link.create("dependency", current_sent_node, root_node, dependency_type="root"))

            for token in sent:
                for child in token.children:
                    dep_link = Link.create("dependency", token._.token_node, child._.token_node,
                                           dependency_type=child.dep_)
                    self.add_link(dep_link)

            last_sent_node = current_sent_node

    def process_linked_entities(self, doc):
        for linked_entity in doc._.linkedEntities:
            entity_span = linked_entity.get_span()

            main_np = entity_span.root._.token_node.find_in_nodes(type="np") \
                .filter(custom=lambda np: np.full_text == ' '.join([t.text for t in entity_span])).first()

            if main_np is not None:
                self.create_decorator_node(source_node=main_np, node_type="linked_entity",
                                           entity_id=linked_entity.get_id(),
                                           entity_label=linked_entity.get_label())

    def process_coref_pipeline(self, doc):
        successful_coref_resolutions = 0
        failed_coref_resolutions = 0
        for coref_cluster in doc._.coref_clusters:
            main_cluster = coref_cluster.main

            # ensure that cluster [Paul McCartney] is not matched with [Paul McCartney and his wife] by matching the full_text of the np with the span from the cluster
            main_np = main_cluster.root._.token_node.find_in_nodes(type="np") \
                .filter(custom=lambda np: np.full_text == ' '.join([t.text for t in main_cluster])).first()

            if main_np is not None:
                for reference in coref_cluster:
                    if reference == main_cluster:
                        continue
                    reference_np = doc[reference.root.i]._.token_node.find_in_nodes(type="np").first()

                    if reference_np is None:
                        if DEBUG:
                            print("reference_np is None: '{} (index {})' ".format(reference, reference[0].i))
                        failed_coref_resolutions += 1
                    else:
                        self.add_link(Link.create("coref", source=reference_np, target=main_np))
                        successful_coref_resolutions += 1
        if DEBUG:
            print("successful coref resolutions: {}".format(successful_coref_resolutions))
            print("failed ner coref: {}".format(failed_coref_resolutions))

    def process_ner_labels(self, doc):
        successful_coref_resolutions = 0
        failed_coref_resolutions = 0
        for coref_cluster in doc._.coref_clusters:
            main_cluster = coref_cluster.main

            # ensure that cluster [Paul McCartney] is not matched with [Paul McCartney and his wife] by matching the full_text of the np with the span from the cluster
            main_np = main_cluster.root._.token_node.find_in_nodes(type="np") \
                .filter(custom=lambda np: np.full_text == ' '.join([t.text for t in main_cluster])).first()

            if main_np is not None:
                for reference in coref_cluster:
                    if reference == main_cluster:
                        continue
                    reference_np = doc[reference.root.i]._.token_node.find_in_nodes(type="np").first()

                    if reference_np is None:
                        if DEBUG:
                            print("reference_np is None: '{} (index {})' ".format(reference, reference[0].i))
                        failed_coref_resolutions += 1
                    else:
                        self.add_link(Link.create("coref", source=reference_np, target=main_np))
                        successful_coref_resolutions += 1
        if DEBUG:
            print("successful coref resolutions: {}".format(successful_coref_resolutions))
            print("failed ner coref: {}".format(failed_coref_resolutions))

    def process_constituency_nodes(self):
        constituency_transformer = ConstituentTransformer()
        constituency_transformer(self)

    @staticmethod
    def from_spacy_doc(doc):
        graph = OpenKnowledgeGraph()
        graph._doc = doc
        '''
        DEPENDENCY TREE
        '''
        graph.process_dependency_nodes(doc)

        '''
        CONSTITUENT TREE
        '''

        graph.process_constituency_nodes()

        '''
        COREF DATA
        '''
        graph.process_coref_pipeline(doc)

        '''
        INDEPENDENT CLAUSE
        '''
        indepClauseTransformer = IndependentClauseTransformer()
        indepClauseTransformer(graph)

        '''
        NER TAGS
        '''
        graph.process_ner_labels(doc)

        pp_type_transformer = PPTypeTransformer()
        pp_type_transformer(graph)

        '''
        LINKED_ENTITIES
        '''
        graph.process_linked_entities(doc)

        return graph

    # merges other graph nodes inline
    def merge(self, other_graph):
        duplicate_nodes = [node for node in other_graph.get_nodes() if node.get_id() in self.nodes_by_id]
        duplicate_links = [link for link in other_graph.get_links() if link.get_id() in self.link_dictionary]

        if len(duplicate_links) > 0 or len(duplicate_nodes) > 0:
            print("found {} duplicate nodes and {} duplicate links".format(len(duplicate_nodes), len(duplicate_links)))
            print(duplicate_nodes)

        for node in other_graph.get_nodes():
            self.add_node(node, override_if_exists=False, assign_id=False)

        for link in other_graph.get_links():
            self.add_link(link, override_if_exists=False, assign_id=False)

        for node_id, property in other_graph.properties_by_node_id.items():
            self.properties_by_node_id[node_id] = property

        return self

    def get_nodes_for_query(self):
        pass

    def get_links_for_query(self):
        pass

    def find_links(self, *queries, **query_args):
        return LinkSelection(self, filter_entities(self.link_dictionary.get_links(), *queries, **query_args))

    def find_nodes(self, *queries, **query_args):
        return NodeSelection(self, filter_entities(self.get_nodes(), *queries, **query_args))

    def fn(self, *queries, **query_args):
        '''
        shortcut for find_nodes
        :param queries:
        :param query_args:
        :return:
        '''
        return self.find_nodes(*queries, **query_args)

    def fl(self, *queries, **query_args):
        '''
        shortcut for find_links
        :param queries:
        :param query_args:
        :return:
        '''

        return self.find_links(*queries, **query_args)

    def serialize(self):
        nodes = {}
        for node in self.get_nodes():
            nodes[node.get_id()] = node.serialize(self)

        links = {}
        for link in self.get_links():
            links[link.get_id()] = link.serialize()

        return {
            "nodes": nodes,
            "links": links
        }

    def save(self, file_path, compressed=True):
        if compressed:
            with bz2.BZ2File(file_path, 'w') as f:
                cPickle.dump(self, f)
        else:
            pickle.dump(self, open(file_path, 'wb'))

    @staticmethod
    def load(file_path, compressed=True):
        if compressed:
            data = bz2.BZ2File(file_path, 'rb')
            data = cPickle.load(data)
            return data
        else:
            return pickle.load(open(file_path, 'rb'))

    def __repr__(self):
        return "<KnowledgeGraph with {} nodes and {} links>".format(len(self.link_dictionary), len(self.get_nodes()))

    @staticmethod
    def from_text(text=None, coref=True, model='en_core_web_md', graph_operations=[]):
        '''
        initializes pipeline
        returns knowledge graph
        :param text:
        :param coref:
        :param model:
        :param graph_operations:
            TODO: specify which operations are executed (e.g. constituency, etc.)
        :return:
        '''
        if model not in PRE_LOADED_PIPELINES_BY_MODEL:
            logging.info("INITIALIZING PIPELINE...")
            nlp = spacy.load('en_core_web_md')
            neuralcoref.add_to_pipe(nlp)
            entityLinker = EntityLinker()
            nlp.add_pipe(entityLinker, last=True, name="entityLinker")

            PRE_LOADED_PIPELINES_BY_MODEL[model] = nlp

        nlp = PRE_LOADED_PIPELINES_BY_MODEL[model]

        return OpenKnowledgeGraph.from_spacy_doc(nlp(text))

    def apply(self, graph_operation: GraphOperation):
        return graph_operation(self)
