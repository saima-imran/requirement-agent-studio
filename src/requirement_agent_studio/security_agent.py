from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.models import Finding, Requirement


class SecurityAgent(BaseAgent):
    """
    Analyses requirements for basic security concerns.
    """

    SECURITY_TERMS = {
        "password": "Specify how passwords must be stored and protected.",
        "login": "Specify authentication and access-control requirements.",
        "encrypted": "Specify the encryption algorithm or security standard.",
    }

    def analyse(self, requirement: Requirement) -> list[Finding]:
        findings = []
        requirement_text = requirement.text.lower()

        for term, suggestion in self.SECURITY_TERMS.items():
            if term in requirement_text:
                findings.append(
                    Finding(
                        requirement_id=requirement.requirement_id,
                        agent_name="SecurityAgent",
                        severity="high",
                        message=(
                            f"The security-related term '{term}' needs "
                            "more implementation-independent detail."
                        ),
                        suggestion=suggestion,
                    )
                )

        return findings
    