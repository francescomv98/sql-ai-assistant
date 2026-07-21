class SQLAssistantError(Exception):
    """Base exception."""

class DatabaseConnectionError(SQLAssistantError):
    """Raised when the database cannot be reached."""

class SQLGenerationError(SQLAssistantError):
    """Raised when the LLM cannot generate SQL."""

class QueryExecutionError(SQLAssistantError):
    """Raised when SQL execution fails."""

class LLMError(SQLAssistantError):
    """Raised when the language model fails."""

class SQLAgentError(SQLAssistantError):
    """Raised when the SQL agent execution fails."""