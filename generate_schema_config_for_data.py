#!/usr/bin/env python
# coding: utf-8

import yaml

from patient_kg.adapters.node_data_classes import Node

mapping_file_path = "./data/mapping.yaml" # "./data/example_input/mapping.yaml"
with open(mapping_file_path, 'r') as yaml_file:
    dataset_mapping = yaml.safe_load(yaml_file)

print(f"Number of nodes {len(dataset_mapping['Nodes'])}")
print(f"Number of edges {len(dataset_mapping['Edges'])}")

schema_config_data = {}

for defined_node in dataset_mapping["Nodes"]:
    node_config = dataset_mapping["Nodes"][defined_node]
    coding_system = node_config["coding_system"]
    id_in_coding_system = node_config["id_in_coding_system"]
    object_type = node_config["object_type"]

    node = Node.create_instance(id_in_coding_system, None, {}, coding_system, object_type)
    node_label = node.get_label()
    
    if node_label == "nan":
        node_label = defined_node

    # Hack for directly inserted columns without mapping (which could contain ', which is not possible for neo4j)
    node_label = node_label.replace("'", "")
        
    schema_config_data[node_label] = {
        "represented_as": "node",
        "preferred_id": coding_system,
        "input_label": node_label
    }
    
    # OPS has no underlying ontology 
    # handle by using explicit inheritance
    if (node_label == node.get_id()) and coding_system == 'ops':
        schema_config_data[node_label]["is_a"] = "OPS"

    # Loinc ontology not yet working 
    # handle by using explicit inheritance
    if (node_label == node.get_id()) and coding_system == 'loinc':
        schema_config_data[node_label]["is_a"] = "loinc"

    # terms with missing mapping to ontology
    # handle by using explicit inheritance
    if coding_system == 'not_mapped_to_ontology':
        schema_config_data[node_label]["is_a"] = "notmappedtoontology"

for edge in dataset_mapping["Edges"]:
    edge_config = dataset_mapping["Edges"][edge]

    # TODO: check if nodes exist
    #source_node = dataset_mapping["Edges"][edge]["source_node"]
    #target_node = dataset_mapping["Edges"][edge]["target_node"]

    #source_node_id = dataset_mapping["Nodes"][source_node]["id_in_coding_system"]
    #target_node_id = dataset_mapping["Nodes"][target_node]["id_in_coding_system"]

    #source_node_label
    #target_node_label
    
    schema_config_data[edge] = {
        "is_a": "concept model attribute (attribute)",
        "represented_as": "edge",
        "input_label": edge,
    }

    if edge_config.get("properties") is not None:
        properties = {}
        for property in edge_config["properties"]:
            properties[property] = edge_config["properties"][property]["type"]
        schema_config_data[edge]["properties"] = properties    

file_path = './config/generated_schema_config_for_data.yaml'

with open(file_path, 'w') as yaml_file:
    yaml.dump(schema_config_data, yaml_file, allow_unicode=True)

print(f'YAML file "{file_path}" has been created.')
