class DuplicateEmailError(Exception):
    """Raised when an email is already registered."""


class RoleNotFoundError(Exception):
    """Raised when the default role does not exist."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""


class InvalidTokenError(Exception):
    """Raised when a JWT is invalid, expired, or not a refresh token."""


class DuplicateTempleNameError(Exception):
    """Raised when a temple name already exists."""


class DuplicateTempleSlugError(Exception):
    """Raised when a temple slug already exists."""


class DuplicateCategoryNameError(Exception):
    """Raised when a category name already exists."""


class DuplicateCategorySlugError(Exception):
    """Raised when a category slug already exists."""


class ResourceNotFoundError(Exception):
    """Raised when a requested resource does not exist."""


class BadRequestError(Exception):
    """Raised when a request is invalid."""