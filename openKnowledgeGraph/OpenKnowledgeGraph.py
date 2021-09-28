import bz2
from openKnowledgeGraph.transformers.CorefTransformer import CorefTransformer
from openKnowledgeGraph.transformers.EntityLinkerTransformer import EntityLinkerTransformer
from openKnowledgeGraph.transformers.SpacyTokenTransformer import SpacyTokenTransformer
from openKnowledgeGraph.nodes.NodeDictionary import NodeDictionary
from typing import List
from openKnowledgeGraph.nodes.Node import Node
from openKnowledgeGraph.selections.GraphSelection import GraphSelection
from openKnowledgeGraph.transformers.DependencyTransformer.DependencyTransformer import DependencyTransformer
from openKnowledgeGraph.links.LinkRegistry import LinkRegistry
from openKnowledgeGraph.propertyRegistry.PropertyRegistry import PropertyRegistry
import pickle
import string
from collections import defaultdict
import _pickle as cPickle
import logging

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from openKnowledgeGraph.nodes import NodeRegistry
from openKnowledgeGraph.index.Index import Index
from openKnowledgeGraph.links.LinkDictionary import LinkDictionary
from openKnowledgeGraph.links.Link import Link
from openKnowledgeGraph.selections.LinkSelection import LinkSelection
from openKnowledgeGraph.selections.NodeSelection import NodeSelection
from openKnowledgeGraph.queries.QueryHelper import filter_entities
from openKnowledgeGraph.transformers.ConstituentTransformer import \
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

    def __init__(self, node_dictionary=None, link_dictionary=None, index_to_ids=None):
        if index_to_ids is None:
            index_to_ids = defaultdict(list)
        if link_dictionary is None:
            link_dictionary = LinkDictionary()
        if node_dictionary is None:
            node_dictionary = NodeDictionary()

        self._doc = None  # TODO remove later: only for debugging


        self.index_by_type = Index("type")

        self.node_dictionary=node_dictionary
        self.link_dictionary = link_dictionary

        self.index_to_ids = index_to_ids

        self.id_counter = 0

        #list of all graph operations that were executed
        self._registered_components=[]

        self.node_properties:PropertyRegistry=PropertyRegistry()
        self.link_properties:PropertyRegistry=PropertyRegistry()

        self.init_id_prefix(''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(PREFIX_LENGTH)))

    def has_component(self,dependency):
        return dependency in self._registered_components

    def register_component(self, component_name):
        if component_name in self._registered_components:
            raise ValueError("Component '{}' was already executed on graph".format(component_name))
        self._registered_components.append(component_name)

    def check_dependency(self,component_name : string) -> bool:
        """returns if component was already executed on graph

        Args:
            component_name (string): [description]

        Returns:
            bool: [description]
        """        
        return component_name in self._registered_components

    def init_id_prefix(self, prefix):
        '''
        allows to specify unique prefix in order to avoid id collisions between distinct graphs
        this is important when different graphs of different documents are "merged"
        :param prefix:
        :return:
        '''
        self.id_prefix = prefix

    def generate_new_id(self) -> str:
        id = self.id_counter
        self.id_counter += 1

        return "{}_{}".format(self.id_prefix, id)

    def add_link(self, link, override_if_exists=False, assign_id=False):
        #if assign_id:
        #    link.set_id(self.generate_new_id())
        self.link_dictionary.add(link, override_if_exists=override_if_exists)

    def add_links(self, links, override_if_exists=False):
        for link in links:
            self.add_link(link, override_if_exists=override_if_exists)

    def remove_link(self, link):
        self.link_dictionary.remove(link)

    def get_inlinks_for_node(self, node, query=None, **query_args):
        return filter_entities(self.link_dictionary.get_inlinks_for_node(node), query=query, **query_args)

    def get_outlinks_for_node(self, node, query=None, **query_args):
        return filter_entities(self.link_dictionary.get_outlinks_for_node(node), query=query, **query_args)

    def get_links_for_node(self, node, query=None, **query_args):
        return filter_entities(self.link_dictionary.get_links_for_node(node), query=query, **query_args)

    def get_node(self, node_id):
        return self.node_dictionary[node_id]

    def get_link(self, link_id):
        return self.link_dictionary[link_id]

    def add_node(self, node, override_if_exists=False, assign_id=True):
        node_exists = node.get_id() in self.node_dictionary
        if node_exists and DEBUG:
            print("WARNING: node id already in graph: ", node)

        if not node_exists or override_if_exists:
            #if assign_id:
            #    node.set_id(self.generate_new_id())
            self.node_dictionary[node.get_id()] = node
            # self.indices += node.get_indices()
        if not node_exists:
            self.index_by_type.add_entry(node.get_type(), node)

    def get_links_for_nodes(self, nodes):
        return [link for link in self.link_dictionary.get_links() if
                link.get_source() in nodes or link.get_target() in nodes]

    def get_property_for_node(self,node_id:str,key:str):
        return self.node_properties.get_property_for_id(id=node_id,key=key)

    def get_properties_for_node(self, node_id:str):
        return self.node_properties.get_properties_for_id(id=node_id)

    def get_properties_for_link(self, link_id:str):
        return self.link_properties.get_properties_for_id(id=link_id)

    def node_has_property(self,node_id:str, key:str):
        return self.node_properties.has_property(node_id,key)

    def node_has_computed_property(self, node_id:str, key:str):
        return self.node_properties.has_computed_property(node_id, key)

    def link_has_property(self,link_id:str,key:str):
        return self.link_properties.has_property(link_id, key)

    def set_property_for_node(self,node_id:str,key:str,value):
        self.node_properties.set_property_for_id(id=node_id,key=key,value=value)

    def register_computed_property_for_node(self,node_id:str,computed_property_name:str):
        self.node_properties.register_computed_property_for_id(id=node_id,key=computed_property_name)

    def get_computed_property_for_node(self,node_id:str, computed_property_name:str):
        if self.node_properties.has_computed_property(node_id, computed_property_name):
            return self.get_node(node_id).__getattribute__(computed_property_name)

    def set_property_for_link(self,link_id:str,key:str,value):
        self.link_properties.set_property_for_id(id=link_id,key=key,value=value)

    def get_property_for_link(self,link_id:str,key:str):
        return self.link_properties.get_property_for_id(id=link_id,key=key)
    
    def draw_node_connections(self, scale_factor=1., save=False, filter_nodes=lambda node: True,
                              filter_entities=lambda link: True):
        DISTANCE_FACTOR = 3.
        MIN_NODE_SIZE = 1000
        MAX_NODE_SIZE = 2000

        NODE_COLORS_BY_TYPE = defaultdict(lambda: "grey", {
            "token":"grey",
            "vp":"red"
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

        edge_list = [(link.get_source().id, link.get_target().id) for link in self.link_dictionary.get_links() if
                     filter_entities(link)]
        G = nx.Graph()
        for node in self.node_dictionary.get_nodes():
            G.add_node(node.get_id())

        G.add_edges_from(edge_list)

        count_inlinks_by_node = []
        for node_id in G.nodes:
            if node_id in self.node_dictionary:
                count_inlinks_by_node.append(len(self.get_node(node_id).find_in_links()))
            else:
                count_inlinks_by_node.append(1)

        min_count_inlinks = min(count_inlinks_by_node)
        max_count_inlinks = max(count_inlinks_by_node)
        node_sizes = []
        labeldict = defaultdict(lambda: 'undefined')
        for node_id in G.nodes:

            if node_id in self.node_dictionary:
                count_inlinks = len(self.get_node(node_id).find_in_links())
                node_sizes.append(MIN_NODE_SIZE + MAX_NODE_SIZE * (count_inlinks / (1 + max_count_inlinks)) / (
                        (min_count_inlinks + 1) / (1 + max_count_inlinks)))
                labeldict[node_id] = self.node_dictionary[node_id].get_text()
            else:
                node_sizes.append(MIN_NODE_SIZE)
                labeldict[node_id] = "undefined"

        color_map_nodes = []
        for node_id in G:
            if node_id in self.node_dictionary:
                color_map_nodes.append(NODE_COLORS_BY_TYPE[self.node_dictionary[node_id].type])
            else:
                color_map_nodes.append('grey')

        color_map_edges = []
        width_map_edges = []
        for link in self.link_dictionary.get_links():
            color_map_edges.append(EDGE_COLORS_BY_TYPE[link.type])
            width_map_edges.append(EDGE_WIDTHS_BY_TYPE[link.type])

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

    def create_link(self, link_type, source, target, **kwargs):
        properties=kwargs
        if properties is None:
            properties = {}
        LinkClass = NodeRegistry.get_by_type(link_type)

        link_id=self.generate_new_id()
        
        LinkClass = LinkRegistry.get_by_type(type)

        if source is None:
            raise ValueError("source is None")
        if target is None:
            raise ValueError("target is None")

        if not source.has_id():
            raise ValueError(
                "Cannot add link: source has has no id (probably because it was not yet added to the KnowledgeGraph)")
        if not target.has_id():
            raise ValueError(
                "Cannot add link: target has has no id (probably because it was not yet added to the KnowledgeGraph)")

        new_link=None
        if LinkClass is None:
            from openKnowledgeGraph.links.Link import Link
            LinkClass=Link

        new_link=LinkClass(
            **{
                **properties,
                'id':link_id,
                'graph':self,
                'type':link_type,
                'source_id': source.get_id(),
                'target_id':target.get_id()
            }
        )

        for computed_property in LinkClass.computed_properties:
            self.register_computed_property_for_node(new_link.get_id(), computed_property)

        self.add_link(new_link)

        for prop,value in properties.items():
            if prop=='id':
                continue
            self.set_property_for_link(link_id,prop,value)

        return new_link


    def cl(self,*args,**kwargs):
        '''
        alias for create_link
        '''
        return self.create_link(*args,**kwargs)

    def create_node(self, node_type, properties=None):
        if properties is None:
            properties = {}
        NodeClass = NodeRegistry.get_by_type(node_type)

        node_id=self.generate_new_id()


        if NodeClass is None:
            from openKnowledgeGraph.nodes.Node import Node
            NodeClass=Node
            
        new_node = NodeClass(
            **{**properties,'id':node_id,'graph':self,'type':node_type}
        )
        for computed_property in NodeClass.computed_properties:
            self.register_computed_property_for_node(new_node.get_id(), computed_property)

        self.add_node(new_node)

        for prop,value in properties.items():
            if prop=='id':
                continue
            self.set_property_for_node(node_id,prop,value)

        #self.properties_by_node_id[new_node.get_id()] = properties

        if len(list(self.node_properties.properties_by_id[node_id].keys()))==0:
            raise Exception()

        return new_node

    def cn(self,*args,**kwargs):
        '''
        alias for create_node
        '''
        return self.create_node(*args,**kwargs)

    def create_decorator_node(self, source_node, node_type, properties=None):
        decorator_node = self.create_node(node_type, properties)
        self.create_link("decorator",source=decorator_node, target=source_node)

        return decorator_node

    def create_reference_node(self, reference_node, node_type, properties=None):
        new_node = self.create_node(node_type, properties)
        self.create_link(link_type="reference", source=new_node, target=reference_node)

        return new_node

    def crn(self,*args,**kwargs):
        ''''
        alias for create_reference_node
        '''
        return self.create_reference_node(*args,**kwargs)


    @staticmethod
    def from_spacy_doc(doc,components=None):
        if components is None:
            components=[
                "token",
                "dependency",
                "coreference",
                "independent_clause",
                "ner"
            ]
        
        graph = OpenKnowledgeGraph()
        graph._doc = doc

        if 'token' in components:
            spacy_token_transformer=SpacyTokenTransformer()
            spacy_token_transformer(graph=graph,doc=doc)

        if 'dependency' in components: 
            dependency_transformer=DependencyTransformer()
            dependency_transformer(graph)

        if 'constituent' in components: 
            constituency_transformer = ConstituentTransformer()
            constituency_transformer(graph)

        if 'coref' in components:
            coref_transformer=CorefTransformer()
            coref_transformer(graph=graph, doc=doc)

        if 'independent' in components:
            indepClauseTransformer = IndependentClauseTransformer()
            indepClauseTransformer(graph)

        if 'entity_linker' in components:
            entity_linker_transformer=EntityLinkerTransformer()
            entity_linker_transformer(graph=graph,doc=doc)

        return graph

    # merges other graph nodes inline
    def merge(self, other_graph):
        duplicate_nodes = [node for node in other_graph.get_nodes() if node.get_id() in self.node_dictionary]
        duplicate_links = [link for link in other_graph.get_links() if link.get_id() in self.link_dictionary]

        if len(duplicate_links) > 0 or len(duplicate_nodes) > 0:
            print("found {} duplicate nodes and {} duplicate links".format(len(duplicate_nodes), len(duplicate_links)))
            print(duplicate_nodes)

        for node in other_graph.get_nodes():
            self.add_node(node, override_if_exists=False, assign_id=False)

        for link in other_graph.get_links():
            self.add_link(link, override_if_exists=False, assign_id=False)

        return self

    def get_nodes(self, node_ids=None):
        return self.node_dictionary.get_nodes(node_ids=node_ids)

    def get_links(self, link_ids=None):
        return self.link_dictionary.get_links(link_ids=link_ids)

    def get_nodes_for_query(self):
        pass

    def get_links_for_query(self):
        pass

    def find_links(self, query=None, **query_args):
        return LinkSelection(self, filter_entities(self.link_dictionary.get_links(), query=query, **query_args))

    def find_nodes(self, query=None, **query_args):
        return NodeSelection(self, filter_entities(self.node_dictionary.get_nodes(), query=query, **query_args))

    def fn(self, query=None, **query_args):
        '''
        shortcut for find_nodes
        :param queries:
        :param query_args:
        :return:
        '''
        return self.find_nodes(query=query, **query_args)

    def fl(self, query=None, **query_args):
        '''
        shortcut for find_links
        :param queries:
        :param query_args:
        :return:
        '''

        return self.find_links(query=query, **query_args)

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
        return "<KnowledgeGraph with {} nodes and {} links>".format(len(self.node_dictionary), len(self.link_dictionary))

    @staticmethod
    def from_text(text=None,model='en_core_web_md',components=None):
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

        return OpenKnowledgeGraph.from_spacy_doc(nlp(text),components=components)

    def apply(self, graph_operation: GraphOperation):
        return graph_operation(self)
