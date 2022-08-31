import re


class NotFoundError(Exception):
    """Requested entity not found."""


class UnexpectedError(Exception):
    """Unexpected error."""


class DatabaseException(Exception):
    """Errors related with database"""


class ApiNotImplementedError(Exception):
    """API not implemented error."""


class NotAuthorizedError(Exception):
    """User not authorized."""


class BadRequestError(Exception):
    """Request error."""


class AppException(Exception):
    """ Main Exception for the app"""


class IntegrityErrorException(Exception):

    @staticmethod
    def parse_exception_message(message: str):
        """Parses a message like  Key (att_name)=(value) already exists. and return attribute name and value
        :param message:
        :return:
        """
        return message

    def __init__(self, message):
        # message will have this type of message 'Key (att_name)=(value) already exists.'
        self.message = self.parse_exception_message(message.message_primary)
        super().__init__(message)
