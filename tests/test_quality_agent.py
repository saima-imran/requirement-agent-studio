from requirement_agent_studio.models import Requirement
from requirement_agent_studio.quality_agent import QualityAgent


def test_detects_ambiguous_term():
    requirement = Requirement(
        requirement_id="REQ-001",
        text="The system should be fast.",
    )

    findings = QualityAgent().analyse(requirement)

    assert len(findings) == 1
    assert findings[0].agent_name == "QualityAgent"
    assert findings[0].severity == "medium"

    