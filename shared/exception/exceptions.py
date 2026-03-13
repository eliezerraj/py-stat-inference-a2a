# exception/exceptions.py

class A2ARequestError(Exception):
    """Raised when an incoming A2A request is invalid."""

class A2ARouterError(A2ARequestError):
    """Raised when an A2A Router message is not supported."""
