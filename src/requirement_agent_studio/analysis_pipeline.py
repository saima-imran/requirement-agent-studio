from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.models import Finding, Requirement


class AnalysisPipeline:
    """
    Runs multiple analysis agents on a collection of requirements.
    """

    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents

    def run(self, requirements: list[Requirement]) -> list[Finding]:
        findings = []

        for requirement in requirements:
            for agent in self.agents:
                findings.extend(agent.analyse(requirement))

        return findings
    