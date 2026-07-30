class ConfigurationError(Exception):
    """
    Raised when a configuration file cannot be loaded correctly.
    """

    pass


class AIModelError(Exception):
    """
    Raised when communication with a language model fails.
    """

    pass


