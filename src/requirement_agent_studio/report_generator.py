from pathlib import Path

from requirement_agent_studio.models import Finding, Requirement


class MarkdownReportGenerator:
    """
    Generates a Markdown report from requirements and findings.
    """

    def generate(
        self,
        requirements: list[Requirement],
        findings: list[Finding],
        output_path: Path,
    ) -> None:
        lines = [
            "# Requirement Analysis Report",
            "",
            f"Total requirements: {len(requirements)}",
            f"Total findings: {len(findings)}",
            "",
        ]

        for requirement in requirements:
            lines.append(f"## {requirement.requirement_id}")
            lines.append("")
            lines.append(f"**Requirement:** {requirement.text}")
            lines.append("")

            requirement_findings = [
                finding
                for finding in findings
                if finding.requirement_id == requirement.requirement_id
            ]

            if not requirement_findings:
                lines.append("No findings.")
                lines.append("")
                lines.append("---")
                lines.append("")
                continue

            for finding in requirement_findings:
                lines.append(f"### {finding.agent_name}")
                lines.append("")
                lines.append(f"**Severity:** {finding.severity.capitalize()}")
                lines.append("")
                lines.append(f"**Issue:** {finding.message}")
                lines.append("")
                lines.append(f"**Suggestion:** {finding.suggestion}")
                lines.append("")

            lines.append("---")
            lines.append("")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")