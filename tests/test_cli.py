from typer.testing import CliRunner

from citation_agent import cli


def test_verify_runtime_error_exit(monkeypatch, tmp_path):
    failing_message = "Service boom"

    class FailingService:
        def __init__(self, config):  # pragma: no cover - simple stub
            pass

        def run(self, file_path):
            raise RuntimeError(failing_message)

    monkeypatch.setattr(cli, "CitationAgentService", FailingService)

    document_path = tmp_path / "brief.txt"
    document_path.write_text("Example content")

    runner = CliRunner()
    result = runner.invoke(cli.app, ["verify", str(document_path)])

    assert result.exit_code == 1
    assert failing_message in result.stdout
