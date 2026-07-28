from pathlib import Path

from requirement_agent_studio.models import Finding, Requirement
from requirement_agent_studio.report_generator import MarkdownReportGenerator


def test_report_generator_creates_markdown_file(tmp_path: Path):
    requirements = [
        Requirement(
            requirement_id="REQ-001",
            text="The system should be fast.",
        )
    ]

    findings = [
        Finding(
            requirement_id="REQ-001",
            agent_name="QualityAgent",
            severity="medium",
            message="The term 'fast' is ambiguous.",
            suggestion="Use a measurable performance criterion.",
        )
    ]

    output_path = tmp_path / "analysis_report.md"

    generator = MarkdownReportGenerator()
    generator.generate(
        requirements=requirements,
        findings=findings,
        output_path=output_path,
    )

    report_content = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert "# Requirement Analysis Report" in report_content
    assert "REQ-001" in report_content
    assert "QualityAgent" in report_content
    assert "The term 'fast' is ambiguous." in report_content


    