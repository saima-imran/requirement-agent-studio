from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.models import Finding, Requirement


class QualityAgent(BaseAgent):
    """
    Analyses requirements for common quality problems.
    """

    AMBIGUOUS_TERMS = {
        "fast",
        "user friendly",
        "easy",
        "quick",
        "efficient",
        "simple",
    }

    def analyse(self, requirement: Requirement) -> list[Finding]:
        findings = []
        requirement_text = requirement.text.lower()

        for term in self.AMBIGUOUS_TERMS:
            if term in requirement_text:
                findings.append(
                    Finding(
                        requirement_id=requirement.requirement_id,
                        agent_name="QualityAgent",
                        severity="medium",
                        message=f"The term '{term}' is ambiguous.",
                        suggestion=(
                            "Replace it with a measurable and testable criterion."
                        ),
                    )
                )

        return findings
    
    