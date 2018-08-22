"""Response descriptions for HTTP responses."""
from typing import Tuple, Type

from rest_framework.exceptions import APIException


def default_desc(exception: Type[APIException]) -> Tuple[int, str]:
    """Get the default response description for an exception.

    Args:
        exception:
            A subclass of APIException for which the response description
            should be returned.

    Returns:
        A tuple containing the matching status code and default description
        for the exception.

    """
    return exception.status_code, str(exception.default_detail)
