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
        ("419620001", "death (event)", {}),
        ("442476006", "arterial oxygen saturation (observable entity)", {}),
        ("1086007", "female structure (body structure)", {}),
        ("26449-9", "26449-9", {}),
        ("59542-1", "59542-1", {}),
        ("21702-6", "21702-6", {}),
        (
            "B95",
            "streptococcus, staphylococcus, and enterococcus as the cause of diseases classified elsewhere",
            {},
        ),
        ("A02", "other salmonella infections", {}),
        ("C01", "malignant neoplasm of base of tongue", {}),
        ("1-100", "1-100", {}),
        ("not_mapped_binary_value", "not_mapped_binary_value", {}),
        ("not_mapped_continuous_value", "not_mapped_continuous_value", {}),
        ("not_mapped_categorical_value", "not_mapped_categorical_value", {}),
    ]
    for node in nodes:
        assert node in expected_nodes

    expected_edges = [
        ("E0", "116154003_2", "1086007", "HAS_CLINICAL_PARAMETER_BINARY", {}),
        ("E1", "116154003_4", "1086007", "HAS_CLINICAL_PARAMETER_BINARY", {}),
        (
            "E2",
            "116154003_1",
            "445320007",
            "HAS_CLINICAL_PARAMETER_CONTINUOUS",
            {"value": 150.0},
        ),
        (
            "E3",
            "116154003_2",
            "445320007",
            "HAS_CLINICAL_PARAMETER_CONTINUOUS",
            {"value": 164.0},
        ),
        (
            "E4",
            "116154003_1",
            "419620001",
            "HAS_CLINICAL_PARAMETER_CONTINUOUS",
            {"value": 1.0},
        ),
        (
            "E5",
            "116154003_2",
            "419620001",
            "HAS_CLINICAL_PARAMETER_CONTINUOUS",
            {"value": 0.0},
        ),
        (
            "E6",
            "116154003_1",
            "442476006",
            "HAS_CLINICAL_PARAMETER_CONTINUOUS",
            {"value": 97.0},
        ),
        (
            "E7",
            "116154003_2",
            "442476006",
            "HAS_CLINICAL_PARAMETER_CONTINUOUS",
            {"value": 96.0},
        ),
        (
            "E8",
            "116154003_4",
            "442476006",
            "HAS_CLINICAL_PARAMETER_CONTINUOUS",
            {"value": 94.0},
        ),
        ("E9", "116154003_1", "21702-6", "HAS_LAB_VALUE_BINARY", {}),
        (
            "E10",
            "116154003_1",
            "26449-9",
            "HAS_LAB_VALUE_CONTINUOUS",
            {"value": 0.11},
        ),
        (
            "E11",
            "116154003_2",
            "26449-9",
            "HAS_LAB_VALUE_CONTINUOUS",
            {"value": 0.12},
        ),
        (
            "E12",
            "116154003_4",
            "26449-9",
            "HAS_LAB_VALUE_CONTINUOUS",
            {"value": 0.14},
        ),
        (
            "E13",
            "116154003_1",
            "59542-1",
            "HAS_LAB_VALUE_CATEGORICAL",
            {"value": 1.0},
        ),
        (
            "E14",
            "116154003_2",
            "59542-1",
            "HAS_LAB_VALUE_CATEGORICAL",
            {"value": 2.0},
        ),
        (
            "E15",
            "116154003_4",
            "59542-1",
            "HAS_LAB_VALUE_CATEGORICAL",
            {"value": 3.0},
        ),
        ("E16", "116154003_2", "B95", "HAS_DISEASE", {}),
        ("E17", "116154003_1", "A02", "HAS_DISEASE", {}),
        ("E18", "116154003_2", "A02", "HAS_DISEASE", {}),
        ("E19", "116154003_3", "C01", "HAS_DISEASE", {}),
        ("E20", "116154003_1", "1-100", "HAS_TREATMENT", {}),
        ("E21", "116154003_2", "1-100", "HAS_TREATMENT", {}),
        (
            "E22",
            "116154003_1",
            "not_mapped_binary_value",
            "NOT_DEFINED_BINARY",
            {},
        ),
        (
            "E23",
            "116154003_1",
            "not_mapped_continuous_value",
            "NOT_DEFINED_CONTINUOUS",
            {"value": 0.1},
        ),
        (
            "E24",
            "116154003_2",
            "not_mapped_continuous_value",
            "NOT_DEFINED_CONTINUOUS",
            {"value": 0.0},
        ),
        (
            "E25",
            "116154003_1",
            "not_mapped_categorical_value",
            "NOT_DEFINED_CATEGORICAL",
            {"value": 1.0},
        ),
        (
            "E26",
            "116154003_2",
            "not_mapped_categorical_value",
            "NOT_DEFINED_CATEGORICAL",
            {"value": 2.0},
        ),
        (
            "E27",
            "116154003_4",
            "not_mapped_categorical_value",
            "NOT_DEFINED_CATEGORICAL",
            {"value": 3.0},
        ),
    ]
    edges = list(adapter.get_edges())
    # order edges by the first element of the tuple
    edges = sorted(edges, key=lambda x: x[0])
    print(edges)
    for edge in edges:
        assert edge in expected_edges
    assert len(edges) == 28
