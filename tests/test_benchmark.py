from sqlsage.eval.benchmark import run_evaluation_benchmark


def test_benchmark_metrics():
    res = run_evaluation_benchmark()
    assert res["execution_accuracy_pct"] == 84.2
    assert res["syntax_validity_pct"] == 100.0
    assert res["hallucination_rate_pct"] == 0.0
    assert res["self_correction_repair_rate_pct"] > 40.0
