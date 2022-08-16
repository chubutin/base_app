import re

from psycopg2._psycopg import Diagnostics


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
