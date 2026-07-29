import pytest

from requirement_agent_studio.config_loader import ConfigLoader
from requirement_agent_studio.exceptions import ConfigurationError


def test_config_loader_loads_configuration():
    config = ConfigLoader.load("quality_rules.json")

    assert isinstance(config, dict)


def test_config_loader_raises_error_for_missing_file():
    with pytest.raises(
        ConfigurationError,
        match="Configuration file not found: missing_rules.json",
    ):
        ConfigLoader.load("missing_rules.json")


        