from fastapi import status


class BusinessRuleException(Exception):
    """
    Raised when a business rule is violated
    (e.g., duplicate recycling, rate limit exceeded).
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        self.message = message
        self.status_code = status_code