from requirement_agent_studio.ai.language_model import LanguageModel
from requirement_agent_studio.ai.quality_analyzer import QualityAIAnalyzer
from requirement_agent_studio.base_agent import BaseAgent
from requirement_agent_studio.config_loader import ConfigLoader
from requirement_agent_studio.exceptions import AIModelError
from requirement_agent_studio.logger import get_logger
from requirement_agent_studio.models import Finding, Requirement

logger = get_logger(__name__)


class QualityAgent(BaseAgent):
    """
    Identifies vague or unmeasurable quality requirements.

    The agent always performs deterministic rule-based analysis.
    AI-assisted analysis is added when a language model is provided.
    """

    def __init__(
        self,
        language_model: LanguageModel | None = None,
    ) -> None:
        self.rules = ConfigLoader.load("quality_rules.json")

        self.ai_analyzer = (
            QualityAIAnalyzer(language_model)
            if language_model is not None
            else None
        )

    def analyse(self, requirement: Requirement) -> list[Finding]:
        logger.info(
            "Starting quality analysis for requirement %s",
            requirement.requirement_id,
        )

        findings = self._analyse_with_rules(requirement)

        if self.ai_analyzer is not None:
            ai_finding = self._analyse_with_ai(requirement)

            if ai_finding is not None:
                findings.append(ai_finding)

        logger.info(
            "Quality analysis completed for requirement %s with %s finding(s)",
            requirement.requirement_id,
            len(findings),
        )

        return findings

    def _analyse_with_rules(
        self,
        requirement: Requirement,
    ) -> list[Finding]:
        """Perform deterministic analysis using configured vague terms."""

        findings: list[Finding] = []
        requirement_text = requirement.text.lower()

        for term in self.rules["vague_terms"]:
            if term in requirement_text:
                findings.append(
                    Finding(
                        requirement_id=requirement.requirement_id,
                        agent_name="QualityAgent",
                        severity=self.rules["severity"],
                        message=f"The term '{term}' is ambiguous.",
                        suggestion=(
                            "Replace it with a measurable and testable criterion."
                        ),
                    )
                )

        return findings

    def _analyse_with_ai(
        self,
        requirement: Requirement,
    ) -> Finding | None:
        """Perform optional structured AI-assisted quality analysis."""

        if self.ai_analyzer is None:
            return None

        try:
            analysis = self.ai_analyzer.analyse(requirement.text)

        except AIModelError as error:
            logger.warning(
                "AI quality analysis failed for requirement %s: %s",
                requirement.requirement_id,
                error,
            )
            return None

        if not analysis.is_ambiguous:
            logger.info(
                "AI analysis found no ambiguity for requirement %s",
                requirement.requirement_id,
            )
            return None

        return Finding(
            requirement_id=requirement.requirement_id,
            agent_name="QualityAgent-AI",
            severity=self.rules["severity"],
            message=(
                f"{analysis.reason} "
                f"AI confidence: {analysis.confidence:.2f}."
            ),
            suggestion=analysis.improved_requirement,
        )

    