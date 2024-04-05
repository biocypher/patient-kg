from biocypher import BioCypher

from patient_kg.adapters.clinical_dataset_adapter import (
    ClinicalDatasetAdapter,
    SnomedCTAdapterEdgeType,
    SnomedCTAdapterNodeType,
)

# Instantiate the BioCypher interface
# You can use `config/biocypher_config.yaml` to configure the framework or
# supply settings via parameters below
bc = BioCypher(
    # biocypher_config_path="config/biocypher_docker_config.yaml",
    biocypher_config_path="config/biocypher_config.yaml",
    # schema_config_path="config/old_schema_config.yaml",
    schema_config_path="config/generated_schema_config_for_data.yaml",
)

# Choose node types to include in the knowledge graph.
# These are defined in the adapter (`adapter.py`).
node_types = [
    SnomedCTAdapterNodeType["PATIENT"],
    SnomedCTAdapterNodeType["SURVIVAL_TIME_DAYS"],
]

# Choose patient adapter fields to include in the knowledge graph.
# These are defined in the adapter (`adapter.py`).
node_fields = [
    # Patients
    # ExampleAdapterPatientField.ID,
    # Survival time
    # ExampleAdapterSurvivalTimeField.ID,
]

edge_types = [
    SnomedCTAdapterEdgeType.PATIENT_TO_SURVIVAL_TIME,
]


base_data_path = "./data"
# Create a snomed ct adapter instance
adapter = ClinicalDatasetAdapter(
    data_file_path=f"{base_data_path}/data.csv",
    mapping_file_path=f"{base_data_path}/mapping.yaml",
    node_types=node_types,
    node_fields=node_fields,
    edge_types=edge_types,
    # TODO: fields and types are not checked for at the moment
    # we can leave edge fields empty, defaulting to all fields in the adapter
)

# Create a knowledge graph from the adapter
bc.write_nodes(adapter.get_nodes())
bc.write_edges(adapter.get_edges())

# Write admin import statement
bc.write_import_call()

# Print summary
# bc.show_ontology_structure(full=True)
# bc.log_missing_input_labels()
# bc.log_duplicates()
bc.summary()
