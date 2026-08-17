from sqlsage.agent.self_correction import SandboxExecutionEngine

def test_sandbox_execution_success():
    sandbox = SandboxExecutionEngine()
    sql = "SELECT count(*) FROM patients;"
    ok, res, err = sandbox.execute_and_verify(sql)
    assert ok is True
    assert res[0][0] == 1

def test_sandbox_execution_failure_and_repair():
    sandbox = SandboxExecutionEngine()
    bad_sql = "SELECT encounter_class, sum(total_claim_cost) FROM encounters"
    ok, res, err = sandbox.execute_and_verify(bad_sql)
    assert ok is False # Missing GROUP BY

    repaired_sql = sandbox.repair_query(bad_sql, err)
    ok_rep, res_rep, err_rep = sandbox.execute_and_verify(repaired_sql)
    assert ok_rep is True
    assert len(res_rep) == 1
