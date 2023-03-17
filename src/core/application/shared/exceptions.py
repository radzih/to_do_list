class ApplicationException(Exception):
    """Base class for all application-level exceptions"""

    @property
    def message(self) -> str:
        return "Application error occurred"


class UnauthorizedUserException(ApplicationException):
    """
    Raised when a user tries to access a resource
    they are not authorized to access
    """

    pass
