class EmailAlreadyExistsError(Exception):
    """Raised when an email address is already registered in the system."""

    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found in the system."""

    pass


class WrongCredentials(Exception):
    """Raised when login credentials are incorrect."""

    pass


class PostNotFoundError(Exception):
    """Raised when a post is not found in the system."""

    pass


class CommentNotFoundError(Exception):
    """Raised when a comment is not found in the system."""

    pass


class UnauthorizedError(Exception):
    """Raised when a user is not authorized to perform an action."""

    pass


class PostAccessDeniedError(Exception):
    """Raised when a user tries to access a private post they don't own."""

    pass
