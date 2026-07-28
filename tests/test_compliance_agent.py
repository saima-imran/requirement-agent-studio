from requirement_agent_studio.compliance_agent import ComplianceAgent
from requirement_agent_studio.models import Requirement


def test_compliance_agent_detects_human_oversight():
    requirement = Requirement(
        requirement_id="REQ-001",
        text="A human operator must be able to override automated decisions."
    )

    agent = ComplianceAgent()
    findings = agent.analyse(requirement)

    assert len(findings) == 1
    assert findings[0].agent_name == "ComplianceAgent"
    assert findings[0].severity == "high"
    assert "Human Oversight" in findings[0].message

    