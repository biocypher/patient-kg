from abc import ABC, abstractmethod

import icd10

from patient_kg.adapters.snomed_ct_api import getConceptById


class Edge(ABC):

    def __init__(self, relationship_id: str, source_node_id: str, target_node_id: str, label: str = None):
        self.relationship_id = str(relationship_id)
        self.source_node_id = str(source_node_id)
        self.target_node_id = str(target_node_id)
        self.label = str(label)

    @abstractmethod
    def tbd(self, id: str):
        pass

    def get_relationship_id(self):
        return self.relationship_id

    def get_source_node_id(self):
        return self.source_node_id

    def get_target_node_id(self):
        return self.target_node_id

    def get_label(self):
        return self.label

    def get_properties(self):
        return {}

    @classmethod
    def create_instance(cls, relationship_id: str, source_node_id: str, target_node_id: str, label: str,
                        properties: dict = None):
        if properties is None or len(properties) == 0:
            return BinaryEdge(relationship_id, source_node_id, target_node_id, label)
        elif properties is not None:
            return WeightedEdge(relationship_id, source_node_id, target_node_id, label, properties)
        else:
            raise ValueError(f"No node class for this edge found ID: {relationship_id}, source node: {source_node_id}, target node: {target_node_id}, label: {label}")


class WeightedEdge(Edge):

    def __init__(self, relationship_id: str, source_node_id: str, target_node_id: str, label: str = None,
                 properties: dict = None):
        super().__init__(relationship_id, source_node_id, target_node_id, label)
        self.properties = properties

    def tbd(self, id: str):
        icd_code = icd10.find(id)
        label_in_input = icd_code.description.lower()
        return label_in_input

    def get_properties(self):
        return self.properties


class BinaryEdge(Edge):

    def tbd(self, id: str):
        label_in_input = getConceptById(str(id)).lower()
        return label_in_input


# Create instances based on the parameter
#instance_A = Edge.create_instance("E1", "1", "2", "edge_1")
#instance_B = Edge.create_instance('E2', "2", "3", "edge2", {"value": 42})
#
#print(instance_A.get_relationship_id())
#print(instance_A.get_source_node_id())
#print(instance_A.get_target_node_id())
#print(instance_A.get_label())
#print(instance_A.get_properties())
#print(instance_B.get_relationship_id())
#print(instance_B.get_source_node_id())
#print(instance_B.get_target_node_id())
#print(instance_B.get_label())
#print(instance_B.get_properties())
