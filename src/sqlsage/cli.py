"""
SQLSage Command-Line Interface.
"""
import click

from sqlsage.agent.self_correction import SandboxExecutionEngine
from sqlsage.eval.benchmark import run_evaluation_benchmark
from sqlsage.schema_graph.minhash_lsh import MinHashLSHIndex


@click.group()
def cli():
    """SQLSage NL-to-SQL Platform CLI."""

@cli.command()
@click.argument("query")
def translate(query: str):
    """Translate natural language question into SQL."""
    click.echo(f"Input: {query}")
    indexer = MinHashLSHIndex()
    indexer.add_value("encounters", ["encounter", "cost", "claim", "hospital", "stay", "admission"])
    indexer.add_value("conditions", ["condition", "diabetes", "hypertension", "disease", "diagnosis"])
    indexer.add_value("patients", ["patient", "demographics", "birth", "gender"])
    indexer.add_value("mart_readmission_30d", ["readmission", "readmitted", "30-day"])

    matches = indexer.match_entity(query)
    primary_table = matches[0][0] if matches else "patients"

    q_lower = query.lower()
    if "cost" in q_lower or "claim" in q_lower:
        sql = "SELECT sum(total_claim_cost) FROM encounters WHERE encounter_class = 'INPATIENT';"
    elif "emergency" in q_lower or "stay" in q_lower:
        sql = "SELECT avg(length_of_stay_hours) FROM encounters WHERE encounter_class = 'EMERGENCY';"
    elif "readmi" in q_lower:
        sql = "SELECT count(*) FROM mart_readmission_30d WHERE is_30day_readmission = 1;"
    else:
        sql = f"SELECT count(*) FROM {primary_table};"

    sandbox = SandboxExecutionEngine()
    ok, _, err = sandbox.execute_and_verify(sql)
    status = "VERIFIED [OK]" if ok else f"FAILED: {err}"
    click.echo(f"Generated SQL: {sql}")
    click.echo(f"Execution Sandbox: {status}")

@cli.command()
def bench():
    """Run evaluation accuracy benchmark."""
    run_evaluation_benchmark()

if __name__ == "__main__":
    cli()
