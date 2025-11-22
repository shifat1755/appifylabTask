class EmailAlreadyExistsError(Exception):
    """Raised when an email address is already registered in the system."""

    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found in the system."""

    pass


class WrongCredentials(Exception):
    """Raised when login credentials are incorrect."""

    pass
