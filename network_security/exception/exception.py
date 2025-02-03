import sys


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys) -> None:
        """
        This is the constructor of the NetworkSecurityException class.

        Args:
            error_message (str): The error message.
            error_details (sys): The error details.
        Returns:
            None
        """
        self.error_message = error_message
        (
            _,
            _,
            exc_tb,
        ) = (
            error_details.exc_info()
        )  # This retrieves the traceback of the current exception.

        self.lineno = (
            exc_tb.tb_lineno
        )  # Extract the line number where the error occurred.
        self.filename = (
            exc_tb.tb_frame.f_code.co_filename
        )  # Extract the filename where the error occurred.

    def __str__(self) -> str:
        """
        This function returns the error message.
        Returns:
            str: The error message.
        """
        error_message = "Error occurred in python script [{0}] line number [{1}] error message [{2}]".format(
            self.filename, self.lineno, str(self.error_message)
        )

        return error_message
