from click.testing import CliRunner

from sqlsage.cli import cli


def test_cli_translate():
    runner = CliRunner()
    res = runner.invoke(cli, ["translate", "count all patients"])
    assert res.exit_code == 0
    assert "Generated SQL" in res.output

def test_cli_bench():
    runner = CliRunner()
    res = runner.invoke(cli, ["bench"])
    assert res.exit_code == 0
    assert "84.2" in res.output
