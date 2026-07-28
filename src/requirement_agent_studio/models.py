from dataclasses import dataclass


@dataclass
class Requirement:
    requirement_id: str
    text: str

@dataclass
class Finding:
    requirement_id: str
    agent_name: str
    severity: str
    message: str
    suggestion: str

@dataclass
class ReviewDecision:
    requirement_id: str
    reviewer: str
    decision: str
    comment: str
    