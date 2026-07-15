class DuplicateEmailError(Exception):
    """Raised when an email is already registered."""


class RoleNotFoundError(Exception):
    """Raised when the default role does not exist."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""