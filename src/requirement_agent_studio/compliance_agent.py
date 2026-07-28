from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.models import Finding, Requirement


class ComplianceAgent(BaseAgent):
    """
    Identifies requirements that may need compliance evidence.
    """

    COMPLIANCE_AREAS = {
        "data": (
            "Data Governance",
            "Document the data source, quality controls, and validation process.",
        ),
        "explanation": (
            "Transparency",
            "Specify what explanation must be provided and to whom.",
        ),
        "human": (
            "Human Oversight",
            "Define when and how a human can review or override the system.",
        ),
        "risk": (
            "Risk Management",
            "Specify how risks will be identified, assessed, and controlled.",
        ),
        "accurate": (
            "Accuracy and Robustness",
            "Define measurable accuracy and robustness criteria.",
        ),
    }

    def analyse(self, requirement: Requirement) -> list[Finding]:
        findings = []
        requirement_text = requirement.text.lower()

        for term, (area, suggestion) in self.COMPLIANCE_AREAS.items():
            if term in requirement_text:
                findings.append(
                    Finding(
                        requirement_id=requirement.requirement_id,
                        agent_name="ComplianceAgent",
                        severity="high",
                        message=(
                            f"This requirement relates to the compliance area "
                            f"'{area}' and may require supporting evidence."
                        ),
                        suggestion=suggestion,
                    )
                )

        return findings
    
    