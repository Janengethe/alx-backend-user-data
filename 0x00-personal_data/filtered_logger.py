#!/usr/bin/env python3
"""
Module filtered_logger
"""
import re
from typing import List
import logging
from os import environ

from mysql.connector import connection

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for f in fields:
        message = re.sub(f + "=.*?" + separator,
                         f + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """
    The logger sis named "user_data" and only log up to logging.INFO level.
    It does not propagate messages to other loggers.
    It have a StreamHandler with RedactingFormatter as formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """returns a connector to the database"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db = environ.get("PERSONAL_DATA_DB_NAME")

    connector = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db)

    return connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using
        filter_datum.
        Values for fields in fields should be filtered.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def main() -> None:
    """
    Obtains a database connection using get_db and retrieve all rows
    in the users table and display each row
    """
    db = get_db()
    cur = db.cursor()

    query = ('SELECT * FROM users;')
    cur.execute(query)
    fetch_data = cur.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        logger.info(fields)

    cur.close()
    db.close()


if __name__ == "__main__":
    """Run"""
    main()
