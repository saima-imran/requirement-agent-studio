from abc import ABC, abstractmethod

from requirement_agent_studio.models import Finding, Requirement


class BaseAgent(ABC):
    """
    Defines the common interface for all requirement-analysis agents.
    """

    @abstractmethod
    def analyse(self, requirement: Requirement) -> list[Finding]:
        """
        Analyse one requirement and return zero or more findings.
        """
        raise NotImplementedError
    