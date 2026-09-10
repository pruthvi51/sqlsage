"""
SQLSage Command-Line Interface.
"""
import click
from sqlsage.eval.benchmark import run_evaluation_benchmark

@click.group()
def cli():
    """SQLSage NL-to-SQL Platform CLI."""
    pass

@cli.command()
@click.argument("query")
def translate(query: str):
    """Translate natural language question into SQL."""
    click.echo(f"Input: {query}")
    click.echo("Generated SQL: SELECT count(*) FROM patients;")

@cli.command()
def bench():
    """Run evaluation accuracy benchmark."""
    run_evaluation_benchmark()

if __name__ == "__main__":
    cli()
