#!/bin/bash -c
cd /usr/app/
cp -r /src/* .
cp config/biocypher_docker_config.yaml config/biocypher_config.yaml
cp config/generated_schema_config_for_data.yaml config/generated_schema_config_for_data.yaml
cp config/ontologies/custom.ttl config/ontologies/custom.ttl
cp config/ontologies/ontology_ICD10CM_patched.ttl config/ontologies/ontology_ICD10CM_patched.ttl
cp config/ontologies/ontology_loinc.ttl config/ontologies/ontology_loinc.ttl
cp config/ontologies/ontology_snomed_ct.owl config/ontologies/ontology_snomed_ct.owl
poetry install
python3 generate_schema_config_for_data.py
python3 create_knowledge_graph.py
chmod -R 777 biocypher-log
