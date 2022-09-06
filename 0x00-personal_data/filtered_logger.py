#!/usr/bin/env python3
"""
FilteredLogger
"""
from typing import List
import logging
import mysql.connector
import os
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ first constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ log generated """
        msg = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ func returns log message obfuscated """
    lt = message.split(separator)

    for j in fields:
        for i in range(len(lt)):
            if lt[i].startswith(j):
                subst = j + '=' + redaction
                lt[i] = re.sub(lt[i], '', lt[i])
                lt[i] = subst
    return separator.join(lt)


def get_logger() -> logging.Logger:
    """
    func takes no arguments and returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    chr = logging.StreamHandler()
    chr.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    chr.setFormatter(formatter)
    logger.addHandler(chr)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function returns a connector to a database """
    cee = mysql.connector.connection.MySQLConnection(
      user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
      password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
      host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
      database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return cee


def main():
    """ main func """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        msge = "name={}; email={}; phone={}; ssn={}; password={};\
ip={}; last_login={}; user_agent={}; ".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        )
        msge = filter_datum(list(PII_FIELDS), '***', msge, '; ')
        logger.info(msge)
    cursor.close()
    db.close()


if __name__ == '__main__':
    """ the main func should run when module is executed """
    main()
