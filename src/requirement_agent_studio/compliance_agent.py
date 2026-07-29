from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.config_loader import ConfigLoader
from requirement_agent_studio.logger import get_logger
from requirement_agent_studio.models import Finding, Requirement

logger = get_logger(__name__)


class ComplianceAgent(BaseAgent):
    """
    Identifies requirements that may need compliance evidence.
    """

    def __init__(self):
        self.rules = ConfigLoader.load("compliance_rules.json")

    def analyse(self, requirement: Requirement) -> list[Finding]:
        logger.info(
            "Starting compliance analysis for requirement %s",
            requirement.requirement_id,
        )

        findings = []
        requirement_text = requirement.text.lower()

        for term, rule in self.rules["compliance_areas"].items():
            if term in requirement_text:
                findings.append(
                    Finding(
                        requirement_id=requirement.requirement_id,
                        agent_name="ComplianceAgent",
                        severity=self.rules["severity"],
                        message=(
                            "This requirement relates to the compliance area "
                            f"'{rule['area']}' and may require supporting "
                            "evidence."
                        ),
                        suggestion=rule["suggestion"],
                    )
                )

        logger.info(
            "Compliance analysis completed for requirement %s with %s finding(s)",
            requirement.requirement_id,
            len(findings),
        )

        return findings
    
    