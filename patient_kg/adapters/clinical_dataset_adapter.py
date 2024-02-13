import math
import random
import string
from enum import Enum, auto
from itertools import chain
from typing import Optional
import icd10
import numpy as np

import pandas as pd
import yaml
from biocypher._create import BioCypherNode
from biocypher._logger import logger

from patient_kg.adapters.edge_data_classes import Edge
from patient_kg.adapters.node_data_classes import Node
from patient_kg.adapters.snomed_ct_api import getConceptById

logger.debug(f"Loading module {__name__}.")

# what is needed:
# - enums which holds all node types, node fields, edge types and edge fields
#   -> this can be generated from the config files
#   -> potential problem with multiple adapters: which config file items belong to which adapter?
# - these enums are passed from the main script to the adapter to define, which sources are added


class SnomedCTAdapterNodeType(Enum):
    """
    Define types of nodes the adapter can provide.
    """

    PATIENT = auto()
    SURVIVAL_TIME_DAYS = auto()


class ExampleAdapterPatientField(Enum):
    """
    Define possible fields the adapter can provide for patients.
    """

    # ID = "id"


class ExampleAdapterSurvivalTimeField(Enum):
    """
    Define possible fields the adapter can provide for survival time.
    """

    # ID = "id"


class SnomedCTAdapterEdgeType(Enum):
    """
    Enum for the types of the protein adapter.
    """

    PATIENT_TO_SURVIVAL_TIME = "PATIENT_TO_SURVIVAL_TIME"


class ExampleAdapterPatientToSurvivalTimeEdgeField(Enum):
    """
    Define possible fields the adapter can provide for protein-protein edges.
    """

    SURVIVAL_TIME_DAYS = "SURVIVAL_TIME_DAYS"


class ClinicalDatasetAdapter:
    """
    Example BioCypher adapter. Generates nodes and edges for creating a
    knowledge graph.

    Args:
        node_types: List of node types to include in the result.
        node_fields: List of node fields to include in the result.
        edge_types: List of edge types to include in the result.
        edge_fields: List of edge fields to include in the result.
    """

    def __init__(
        self,
        data_file_path: str,
        mapping_file_path: str,
        node_types: Optional[list] = None,
        node_fields: Optional[list] = None,
        edge_types: Optional[list] = None,
        edge_fields: Optional[list] = None,
    ):
        self._set_types_and_fields(node_types, node_fields, edge_types, edge_fields)
        self.dataset = pd.read_csv(data_file_path)
        # self.dataset = pd.read_excel(data_file_path)
        self.dataset.columns = self.dataset.columns.str.strip()
        # Hack: to make direct insertion of columns wihtout ontology mapping possible
        self.dataset.columns = self.dataset.columns.str.replace("'", "")
        with open(mapping_file_path, 'r') as yaml_file:
            self.dataset_mapping = yaml.safe_load(yaml_file)


    def get_nodes(self):
        """
        Returns a generator of node tuples for node types specified in the
        adapter constructor.
        """
        logger.info("Generating nodes.")

        self.nodes = []

        nodes_to_be_mapped = self.dataset_mapping["Nodes"]

        for node in nodes_to_be_mapped:
            node_config = self.dataset_mapping["Nodes"][node]
            coding_system = node_config["coding_system"]
            id_in_coding_system = node_config["id_in_coding_system"]
            object_type = node_config["object_type"]
            # TODO: handle properties? -> add to config file if needed?

            if object_type == "concept":
                # add node concepts (each column is one node representing one snomedct concept)
                if coding_system == "not_mapped_to_ontology":
                    node = Node.create_instance(node, None, {}, coding_system, object_type)
                else:
                    node = Node.create_instance(str(id_in_coding_system), None, {}, coding_system, object_type)
                self.nodes.append(node)
            elif object_type == "instance":
                # add node instances (each row is an own node)
                for row in self.dataset[node]:
                    node = Node.create_instance(str(id_in_coding_system) + "_" + str(row), None, {}, coding_system, object_type)
                    self.nodes.append(node)

        for node in self.nodes:
            yield (node.get_id(), node.get_label(), node.get_properties())


    def get_edges(self):
        """
        Returns a generator of edge_name tuples for edge_name types specified in the
        adapter constructor.
        """

        logger.info("Generating edges.")

        if not self.nodes:
            raise ValueError("No nodes found. Please run get_nodes() first.")

        edge_id = 0
        edges_to_be_mapped = self.dataset_mapping["Edges"]

        self.edges = set()
        for edge_name in edges_to_be_mapped:
            # Only one case at the moment: instance node -> concept node

            edge_config = self.dataset_mapping["Edges"][edge_name]
            source_node = edge_config["source_node"]
            target_nodes_list = edge_config["target_nodes"]
            defined_properties = edge_config.get("properties")

            if not isinstance(target_nodes_list, list):
                raise TypeError("Target nodes must be defined as a list")

            source_node_id = self.dataset_mapping["Nodes"][source_node]["id_in_coding_system"]
            target_nodes_dict = {}
            for target_node_name in target_nodes_list:
                if self.dataset_mapping["Nodes"][target_node_name]["coding_system"] == "not_mapped_to_ontology":
                    target_nodes_dict[target_node_name] = target_node_name
                else:
                    target_nodes_dict[self.dataset_mapping["Nodes"][target_node_name]["id_in_coding_system"]] = target_node_name

            for target_node_id, target_node_value in target_nodes_dict.items():
                for row_index, row in self.dataset.iterrows():
                    relationship_id = "E" + str(edge_id)
                    edge_id += 1

                    source_node_id_instance = f"{source_node_id}_{int(row[source_node])}"

                    properties = {}
                    if defined_properties is not None:
                        # weighted edge_name
                        for property in defined_properties:
                            if not np.isnan(row[target_node_value]):
                                if defined_properties[property]["type"] == "int":
                                    properties[property] = int(row[target_node_value])
                                elif defined_properties[property]["type"] == "float":
                                    properties[property] = float(row[target_node_value])
                        edge = Edge.create_instance(relationship_id, source_node_id_instance, target_node_id, edge_name, properties)
                    if row[target_node_value] == 1:
                        # binary edge_name
                        edge = Edge.create_instance(relationship_id, source_node_id_instance, target_node_id, edge_name, properties)

                    if edge is not None:
                        # logger.info(f"Adding edge_name {edge.get_relationship_id()}, {edge.get_source_node_id()}, {edge.get_target_node_id()}, {edge.get_label()}, {edge.get_properties()}")
                        self.edges.add(edge)
        for edge in self.edges:
            yield (edge.get_relationship_id(), edge.get_source_node_id(), edge.get_target_node_id(), edge.get_label(), edge.get_properties())


    def get_node_count(self):
        """
        Returns the number of nodes generated by the adapter.
        """
        return len(list(self.get_nodes()))

    def _set_types_and_fields(self, node_types, node_fields, edge_types, edge_fields):
        if node_types:
            self.node_types = node_types
        else:
            self.node_types = [type for type in SnomedCTAdapterNodeType]

        if node_fields:
            self.node_fields = node_fields
        else:
            self.node_fields = [
                field
                for field in chain(
                    ExampleAdapterPatientField,
                    ExampleAdapterSurvivalTimeField,
                )
            ]

        if edge_types:
            self.edge_types = edge_types
        else:
            self.edge_types = [type for type in SnomedCTAdapterEdgeType]

        if edge_fields:
            self.edge_fields = edge_fields
        else:
            self.edge_fields = [field for field in chain()]
