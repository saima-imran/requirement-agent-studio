import json
from pathlib import Path
from typing import Any

from requirement_agent_studio.exceptions import ConfigurationError
from requirement_agent_studio.logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """
    Loads JSON configuration files from the project's config folder.
    """

    @staticmethod
    def load(filename: str) -> dict[str, Any]:
        project_root = Path(__file__).resolve().parents[2]
        config_path = project_root / "config" / filename

        logger.info("Loading configuration: %s", filename)

        try:
            with config_path.open("r", encoding="utf-8") as config_file:
                config = json.load(config_file)

        except FileNotFoundError as error:
            logger.error("Configuration file not found: %s", config_path)

            raise ConfigurationError(
                f"Configuration file not found: {filename}"
            ) from error

        logger.info("Configuration loaded successfully: %s", filename)

        return config

    
    