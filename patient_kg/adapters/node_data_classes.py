from abc import ABC, abstractmethod

import icd10
from biocypher import logger

from patient_kg.adapters.snomed_ct_api import get_snomed_name


class Node(ABC):

    def __init__(self, id: str, label:str=None, properties: dict= None, coding_system: str=None, object_type: str=None):
        self.id = id
        if label is None:
            if object_type == "concept":
                label = self.get_label_from_id(str(self.id))
            elif object_type == "instance":
                concept_id_without_instance_id = str(self.id).rsplit('_', 1)[0]
                label = self.get_label_from_id(concept_id_without_instance_id)
        self.label = label
        if properties is None:
            properties = {}
        self.properties = properties

    @abstractmethod
    def get_label_from_id(self, id: str):
        pass

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_properties(self):
        return self.properties

    @classmethod
    def create_instance(cls, id: str, label: str=None, properties:dict={}, coding_system: str=None, object_type:str="concept"):
        # Choose and create a concrete class based on the parameter
        if coding_system == 'icd10':
            return ICDNode(id, label, properties, coding_system, object_type)
        elif coding_system == 'snomedct':
            return SnomedCTNode(id, label, properties, coding_system, object_type)
        elif coding_system == 'ops':
            return OPSNode(id, label, properties, coding_system, object_type)
        elif coding_system == 'loinc':
            return LoincNode(id, label, properties, coding_system, object_type)
        elif coding_system == 'not_mapped_to_ontology':
            return NotMappedNode(id, label, properties, coding_system, object_type)
        else:
            raise ValueError(f"No node class for {coding_system} coding system")


class ICDNode(Node):
    def get_label_from_id(self, id: str):
        icd_code = icd10.find(id)
        if icd_code:
            label_in_input = icd_code.description.lower()
            return label_in_input
        else:
            logger.warning(f"ICD10 code {id} not found in the icd10 package.")
            return None


class SnomedCTNode(Node):
    def get_label_from_id(self, id: str):
        label_in_input = get_snomed_name(id).lower() # getConceptById(str(id)).lower()
        if label_in_input:
            return label_in_input
        else:
            logger.warning(f"SnomedCT code {id} not found in the snomedct package.")
            return None


class OPSNode(Node):
    def get_label_from_id(self, id: str):
        # TODO: read OPS data here? Or can this be ignored
        return id


class LoincNode(Node):
    def get_label_from_id(self, id: str):
        # TODO
        return id

class NotMappedNode(Node):
    def get_label_from_id(self, id: str):
        return id

#instance_A = Node.create_instance("B90", None, {}, "icd10", "concept")
#instance_B = Node.create_instance('B91_1', None, {}, "icd10", "instance")

#print(instance_A.get_id())
#print(instance_A.label)
#print(instance_A.properties)
#print(instance_B.id)
#print(instance_B.label)
#print(instance_B.properties)
