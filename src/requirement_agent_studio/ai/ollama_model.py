from typing import Any

from ollama import chat

from requirement_agent_studio.ai.language_model import LanguageModel
from requirement_agent_studio.config_loader import ConfigLoader
from requirement_agent_studio.exceptions import AIModelError


class OllamaLanguageModel(LanguageModel):
    """Language-model implementation using a local Ollama server."""

    def __init__(self) -> None:
        config = ConfigLoader.load("ai.json")

        model_name = config.get("model")

        if not isinstance(model_name, str) or not model_name.strip():
            raise AIModelError(
                "The AI configuration must contain a valid model name."
            )

        self.model_name = model_name.strip()

    def generate(
        self,
        prompt: str,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise AIModelError("The AI prompt must not be empty.")

        try:
            response = chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                format=response_format or "json",
                options={
                    "temperature": 0,
                },
            )

        except Exception as error:
            raise AIModelError(
                f"Ollama failed to generate a response: {error}"
            ) from error

        content = response.message.content

        if not isinstance(content, str) or not content.strip():
            raise AIModelError("Ollama returned an empty response.")

        return content.strip()
    