from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.config_loader import ConfigLoader
from requirement_agent_studio.logger import get_logger
from requirement_agent_studio.models import Finding, Requirement

logger = get_logger(__name__)


class QualityAgent(BaseAgent):
    """
    Identifies vague or unmeasurable quality requirements.
    """

    def __init__(self):
        self.rules = ConfigLoader.load("quality_rules.json")

    def analyse(self, requirement: Requirement) -> list[Finding]:
        logger.info(
            "Starting quality analysis for requirement %s",
            requirement.requirement_id,
        )

        findings = []
        requirement_text = requirement.text.lower()

        for term in self.rules["vague_terms"]:
            if term in requirement_text:
                findings.append(
                    Finding(
                        requirement_id=requirement.requirement_id,
                        agent_name="QualityAgent",
                        severity=self.rules["severity"],
                        message=f"The term '{term}' is ambiguous.",
                        suggestion=(
                            "Replace it with a measurable and testable criterion."
                        ),
                    )
                )

        logger.info(
            "Quality analysis completed for requirement %s with %s finding(s)",
            requirement.requirement_id,
            len(findings),
        )

        return findings
    