"""Response descriptions for HTTP responses."""


def default_desc(exception):
    """Get the default response description for an exception.

    Args:
        exception (rest_framework.exceptions.APIException):
            A subclass of APIException for which the response description
            should be returned.

    Returns:
        (int, str):
            A tuple containing the matching status code and default description
            for the exception.

    """
    return exception.status_code, str(exception.default_detail)
