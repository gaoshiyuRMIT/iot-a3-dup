#!/usr/bin/python3

""" The database exception class is for all exeptions occurring
from DB-related errors, or otherwise, to make error
handling clearer in the context of the whole application. """


class DBException(Exception):

    """DBException is designed to catch any type of error in database
    functioning. The arg 'message' must always be supplied and can be
    a custom error message, or the one supplied by the original exception.
    'exception_message' is the error statement supplied by the original
    exception, as is error_code, if available."""
    def __init__(self, message, exception_message=None, error_code=None):
        self.message = message
        if exception_message is not None:
            self.exception_message = exception_message
        if error_code is not None:
            self.error_code = error_code
