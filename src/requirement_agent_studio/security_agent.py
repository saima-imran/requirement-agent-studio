from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.config_loader import ConfigLoader
from requirement_agent_studio.logger import get_logger
from requirement_agent_studio.models import Finding, Requirement

logger = get_logger(__name__)


class SecurityAgent(BaseAgent):
    """
    Identifies requirements that may need stronger security details.
    """

    def __init__(self):
        self.rules = ConfigLoader.load("security_rules.json")

    def analyse(self, requirement: Requirement) -> list[Finding]:
        logger.info(
            "Starting security analysis for requirement %s",
            requirement.requirement_id,
        )

        findings = []
        requirement_text = requirement.text.lower()

        for term, suggestion in self.rules["security_terms"].items():
            if term in requirement_text:
                findings.append(
                    Finding(
                        requirement_id=requirement.requirement_id,
                        agent_name="SecurityAgent",
                        severity=self.rules["severity"],
                        message=(
                            f"The security-related term '{term}' requires "
                            "more detail."
                        ),
                        suggestion=suggestion,
                    )
                )

        logger.info(
            "Security analysis completed for requirement %s with %s finding(s)",
            requirement.requirement_id,
            len(findings),
        )

        return findings
    
    
    


    