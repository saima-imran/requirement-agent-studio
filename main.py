from pathlib import Path

from requirement_agent_studio.analysis_pipeline import AnalysisPipeline
from requirement_agent_studio.compliance_agent import ComplianceAgent
from requirement_agent_studio.extractor_agent import RequirementExtractionAgent
from requirement_agent_studio.models import Requirement
from requirement_agent_studio.quality_agent import QualityAgent
from requirement_agent_studio.report_generator import MarkdownReportGenerator
from requirement_agent_studio.security_agent import SecurityAgent


def main():
    file_path = Path("data/sample_requirements.txt")
    document = file_path.read_text(encoding="utf-8")

    extractor = RequirementExtractionAgent()
    requirements: list[Requirement] = extractor.extract(document)

    pipeline = AnalysisPipeline(
        [
            QualityAgent(),
            SecurityAgent(),
            ComplianceAgent(),
        ]
    )

    findings = pipeline.run(requirements)

    report_generator = MarkdownReportGenerator()
    report_path = Path("output/analysis_report.md")

    report_generator.generate(
        requirements=requirements,
        findings=findings,
        output_path=report_path,
    )

    print(f"\nReport generated: {report_path}")
    print("\nAnalysis Findings\n")

    for finding in findings:
        print(f"Requirement: {finding.requirement_id}")
        print(f"Agent      : {finding.agent_name}")
        print(f"Severity   : {finding.severity}")
        print(f"Issue      : {finding.message}")
        print(f"Suggestion : {finding.suggestion}")
        print()


if __name__ == "__main__":
    main()





