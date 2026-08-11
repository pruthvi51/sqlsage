from sqlsage.constrained_decoding.grammar_mask import GrammarMaskValidator

def test_valid_query():
    schema = {"patients": ["patient_id", "first_name"], "encounters": ["encounter_id", "patient_id"]}
    validator = GrammarMaskValidator(schema)
    sql = "SELECT p.patient_id, p.first_name FROM patients p JOIN encounters e ON p.patient_id = e.patient_id"
    valid, errors = validator.validate_ast(sql)
    assert valid is True
    assert len(errors) == 0

def test_hallucinated_table():
    schema = {"patients": ["patient_id", "first_name"]}
    validator = GrammarMaskValidator(schema)
    sql = "SELECT * FROM billing_records"
    valid, errors = validator.validate_ast(sql)
    assert valid is False
    assert any("billing_records" in e for e in errors)
