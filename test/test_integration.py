from patient_kg.adapters.clinical_dataset_adapter import ClinicalDatasetAdapter


def test_adapter_end_to_end():
    # TODO: not good, that test data is not in the test dir?
    base_data_path = "./data/example_input"
    adapter = ClinicalDatasetAdapter(
        data_file_path=f"{base_data_path}/mock_data.csv",
        mapping_file_path=f"{base_data_path}/mapping.yaml",
    )
    nodes = adapter.get_nodes()
    expected_nodes = [
        ("116154003_1", "patient (person)", {}),
        ("116154003_2", "patient (person)", {}),
        ("116154003_3", "patient (person)", {}),
        ("116154003_4", "patient (person)", {}),
        ("445320007", "survival time (observable entity)", {}),
        ("442476006", "arterial oxygen saturation (observable entity)", {}),
        ("26449-9", "26449-9", {}),
        (
            "B95",
            "streptococcus, staphylococcus, and enterococcus as the cause of diseases classified elsewhere",
            {},
        ),
        ("A02", "other salmonella infections", {}),
        ("C01", "malignant neoplasm of base of tongue", {}),
        ("1-100", "1-100", {}),
        ("not_mapped_discrete_value", "not_mapped_discrete_value", {}),
        ("not_mapped_continuous_value", "not_mapped_continuous_value", {}),
    ]
    for node in nodes:
        assert node in expected_nodes

    expected_edges = [
        (
            "E0",
            "116154003_1",
            "445320007",
            "HAS_CLINICAL_PARAMETER",
            {"value": 150.0},
        ),
        (
            "E1",
            "116154003_2",
            "445320007",
            "HAS_CLINICAL_PARAMETER",
            {"value": 164.0},
        ),
        (
            "E2",
            "116154003_1",
            "442476006",
            "HAS_CLINICAL_PARAMETER",
            {"value": 97.0},
        ),
        (
            "E3",
            "116154003_2",
            "442476006",
            "HAS_CLINICAL_PARAMETER",
            {"value": 96.0},
        ),
        (
            "E4",
            "116154003_4",
            "442476006",
            "HAS_CLINICAL_PARAMETER",
            {"value": 94.0},
        ),
        ("E5", "116154003_1", "26449-9", "HAS_LAB_VALUE", {"value": 0.11}),
        ("E6", "116154003_2", "26449-9", "HAS_LAB_VALUE", {"value": 0.12}),
        ("E7", "116154003_4", "26449-9", "HAS_LAB_VALUE", {"value": 0.14}),
        ("E8", "116154003_2", "B95", "HAS_DISEASE", {}),
        ("E9", "116154003_1", "A02", "HAS_DISEASE", {}),
        ("E10", "116154003_2", "A02", "HAS_DISEASE", {}),
        ("E11", "116154003_3", "C01", "HAS_DISEASE", {}),
        ("E12", "116154003_1", "1-100", "HAS_TREATMENT", {}),
        ("E13", "116154003_2", "1-100", "HAS_TREATMENT", {}),
        (
            "E14",
            "116154003_1",
            "not_mapped_discrete_value",
            "NOT_DEFINED_BINARY",
            {},
        ),
        (
            "E15",
            "116154003_1",
            "not_mapped_continuous_value",
            "NOT_DEFINED_CONTINUOUS",
            {"value": 0.1},
        ),
        (
            "E16",
            "116154003_2",
            "not_mapped_continuous_value",
            "NOT_DEFINED_CONTINUOUS",
            {"value": 0.0},
        ),
    ]
    edges = list(adapter.get_edges())
    for edge in edges:
        assert edge in expected_edges
    assert len(edges) == 17
