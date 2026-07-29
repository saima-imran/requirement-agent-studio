from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.logger import get_logger
from requirement_agent_studio.models import Finding, Requirement

logger = get_logger(__name__)


class AnalysisPipeline:
    """
    Runs multiple analysis agents on a collection of requirements.
    """

    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents

    def run(self, requirements: list[Requirement]) -> list[Finding]:
        logger.info(
            "Starting analysis pipeline with %s requirement(s) and %s agent(s)",
            len(requirements),
            len(self.agents),
        )

        findings = []

        for requirement in requirements:
            logger.info(
                "Starting analysis for requirement %s",
                requirement.requirement_id,
            )

            for agent in self.agents:
                agent_name = agent.__class__.__name__

                logger.info(
                    "Running %s for requirement %s",
                    agent_name,
                    requirement.requirement_id,
                )

                agent_findings = agent.analyse(requirement)
                findings.extend(agent_findings)

                logger.info(
                    "%s completed for requirement %s with %s finding(s)",
                    agent_name,
                    requirement.requirement_id,
                    len(agent_findings),
                )

            logger.info(
                "Completed analysis for requirement %s",
                requirement.requirement_id,
            )

        logger.info(
            "Analysis pipeline completed with %s total finding(s)",
            len(findings),
        )

        return findings

    