import json
from typing import Any

from requirement_agent_studio.ai.language_model import LanguageModel
from requirement_agent_studio.exceptions import AIModelError
from requirement_agent_studio.models import AIQualityAnalysis


class QualityAIAnalyzer:
    """Performs structured AI-assisted requirement quality analysis."""

    RESPONSE_SCHEMA: dict[str, Any] = {
        "type": "object",
        "properties": {
            "is_ambiguous": {
                "type": "boolean",
            },
            "reason": {
                "type": "string",
            },
            "improved_requirement": {
                "type": "string",
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
            },
        },
        "required": [
            "is_ambiguous",
            "reason",
            "improved_requirement",
            "confidence",
        ],
        "additionalProperties": False,
    }

    def __init__(self, language_model: LanguageModel) -> None:
        self.language_model = language_model

    def analyse(self, requirement_text: str) -> AIQualityAnalysis:
        """Analyse one requirement and return a structured result."""

        if not isinstance(requirement_text, str):
            raise AIModelError(
                "The requirement supplied to the AI analyzer must be text."
            )

        if not requirement_text.strip():
            raise AIModelError(
                "The requirement supplied to the AI analyzer must not be empty."
            )

        prompt = self._build_prompt(requirement_text)

        response = self.language_model.generate(
            prompt,
            response_format=self.RESPONSE_SCHEMA,
        )

        return self._parse_response(response)

    def _build_prompt(self, requirement_text: str) -> str:
        """Create the quality-analysis prompt."""

        return (
            "You are a software requirements quality analyst.\n\n"
            "Analyse the following software requirement for ambiguity, "
            "measurability, and testability.\n\n"
            f"Requirement:\n{requirement_text}\n\n"
            "Apply these rules:\n"
            "- Subjective or vague terms such as quickly, efficiently, "
            "user-friendly, easy, sufficient, appropriate, and secure "
            "without definitions make a requirement ambiguous.\n"
            "- A requirement without a measurable threshold, unit, "
            "condition, or acceptance criterion may be ambiguous.\n"
            "- A requirement is not ambiguous when it contains clear, "
            "measurable, and testable criteria.\n"
            "- The reason must agree logically with is_ambiguous.\n"
            "- When is_ambiguous is true, improved_requirement must provide "
            "a specific, measurable, and testable rewrite.\n"
            "- When is_ambiguous is false, improved_requirement may repeat "
            "the original requirement or provide a minor clarification.\n"
            "- Do not use placeholders such as X, Y, TBD, or an unspecified "
            "number.\n"
            "- confidence must be a number between 0.0 and 1.0.\n\n"
            "Classification example:\n"
            'Requirement: "The system should respond quickly."\n'
            'Correct result: "is_ambiguous": true\n'
            'Reason: "The word quickly has no measurable response-time '
            'threshold."\n'
            'Improved requirement: "The system should respond within '
            '2 seconds of receiving user input."\n\n'
            "Return only the JSON object requested by the supplied schema."
        )

    def _parse_response(self, response: str) -> AIQualityAnalysis:
        """Convert the model response into an AIQualityAnalysis object."""

        if not isinstance(response, str) or not response.strip():
            raise AIModelError(
                "The language model returned an empty response."
            )

        try:
            data = json.loads(response)

        except json.JSONDecodeError as error:
            raise AIModelError(
                "The language model returned invalid JSON."
            ) from error

        self._validate_response(data)

        return AIQualityAnalysis(
            is_ambiguous=data["is_ambiguous"],
            reason=data["reason"].strip(),
            improved_requirement=data["improved_requirement"].strip(),
            confidence=float(data["confidence"]),
        )

    def _validate_response(self, data: Any) -> None:
        """Validate the structure and values returned by the model."""

        if not isinstance(data, dict):
            raise AIModelError(
                "The language model response must be a JSON object."
            )

        required_fields = {
            "is_ambiguous",
            "reason",
            "improved_requirement",
            "confidence",
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise AIModelError(
                f"The language model response is missing: {missing}."
            )

        unexpected_fields = data.keys() - required_fields

        if unexpected_fields:
            unexpected = ", ".join(sorted(unexpected_fields))
            raise AIModelError(
                f"The language model response contains unexpected fields: "
                f"{unexpected}."
            )

        if not isinstance(data["is_ambiguous"], bool):
            raise AIModelError(
                "The 'is_ambiguous' field must be a boolean."
            )

        reason = data["reason"]

        if not isinstance(reason, str) or not reason.strip():
            raise AIModelError(
                "The 'reason' field must be a non-empty string."
            )

        improved_requirement = data["improved_requirement"]

        if (
            not isinstance(improved_requirement, str)
            or not improved_requirement.strip()
        ):
            raise AIModelError(
                "The 'improved_requirement' field must be a "
                "non-empty string."
            )

        confidence = data["confidence"]

        if isinstance(confidence, bool) or not isinstance(
            confidence,
            (int, float),
        ):
            raise AIModelError(
                "The 'confidence' field must be a number."
            )

        if not 0.0 <= float(confidence) <= 1.0:
            raise AIModelError(
                "The 'confidence' field must be between 0.0 and 1.0."
            )

        