class EmailAssistantError(Exception):
    """Base class for all domain errors raised by email_assistant."""


class ConfigurationError(EmailAssistantError):
    pass


class GmailAuthenticationError(EmailAssistantError):
    pass


class GmailServiceError(EmailAssistantError):
    pass


class CacheError(EmailAssistantError):
    pass
