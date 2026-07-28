from requirement_agent_studio.models import Requirement
from requirement_agent_studio.security_agent import SecurityAgent


def test_detects_security_term():
    requirement = Requirement(
        requirement_id="REQ-001",
        text="Passwords shall be encrypted.",
    )

    findings = SecurityAgent().analyse(requirement)

    assert len(findings) == 2
    assert all(finding.agent_name == "SecurityAgent" for finding in findings)
    assert all(finding.severity == "high" for finding in findings)