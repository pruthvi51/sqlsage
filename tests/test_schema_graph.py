from sqlsage.schema_graph.graph import SchemaGraph
from sqlsage.schema_graph.minhash_lsh import MinHashLSHIndex

def test_steiner_tree_path():
    sg = SchemaGraph()
    sg.add_table("patients", ["patient_id", "first_name"])
    sg.add_table("encounters", ["encounter_id", "patient_id"])
    sg.add_table("conditions", ["condition_id", "patient_id"])
    sg.add_foreign_key("encounters", "patients", "encounters.patient_id = patients.patient_id")
    sg.add_foreign_key("conditions", "patients", "conditions.patient_id = patients.patient_id")

    sub = sg.extract_connecting_subgraph(["encounters", "conditions"])
    assert "patients" in sub
    assert "encounters" in sub
    assert "conditions" in sub

def test_minhash_entity_match():
    lsh = MinHashLSHIndex()
    lsh.add_value("INPATIENT", ["inpatient", "admitted", "hospitalized"])
    lsh.add_value("EMERGENCY", ["emergency", "er", "urgent"])

    matches = lsh.match_entity("Find all inpatient admissions")
    assert len(matches) > 0
    assert matches[0][0] == "INPATIENT"
