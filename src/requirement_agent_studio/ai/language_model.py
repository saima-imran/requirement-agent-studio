from abc import ABC, abstractmethod
from typing import Any


class LanguageModel(ABC):
    """Abstract interface for language-model providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Generate a response for the supplied prompt."""
        raise NotImplementedError
    