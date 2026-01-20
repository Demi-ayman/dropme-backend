from typing import Any, Optional


def success_response(
    data: Any = None,
    message: str = "Success"
) -> dict:
    """
    Standard success response format
    """
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error_response(
    message: str,
    details: Optional[Any] = None
) -> dict:
    """
    Standard error response format
    """
    response = {
        "status": "error",
        "message": message,
    }

    if details is not None:
        response["details"] = details

    return response