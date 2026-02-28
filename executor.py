"""
This module provides for PostgreSQL database operations.
It uses the psycopg2 library and provides functions for database connectivity and query execution.
"""
import psycopg2

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """
    Create and return a connection to a PostgreSQL database.
    :param db_name:Name of the database to connect to
    :param db_user:Database username for authentication
    :param db_password:Password for the database user
    :param db_host:Hostname of the database server
    :param db_port:Port number the database server is connected to
    :return: psycopg2.connection or None: Database connection object if successful,None if connection fails
    """
    connection_object = None
    try:
        connection_object = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")
    return connection_object

def execute_query(connection, query, values=None):
    """
     Execute a non-SELECT query
    :param connection: Database connection object
    :param query: SQL query to execute
    :param values: tuples of values for parameterized queries. None as Default
    :return: None
    """
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")

def execute_many(connection, query, values=None):
    """
    Execute an INSERT with multiple value  query
    :param connection: Database connection object
    :param query: SQL query to execute
    :param values: list of tuples of values for parameterized queries. None as Default
    :return: None
    """
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.executemany(query, values)
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")

def fetch_one(connection, query, values=None):
    """
     Execute a SELECT query
    :param connection: Database connection object
    :param query: SQL query to execute
    :param values: tuples of values for parameterized queries. None as Default
    :return: tuple result of select query
    """
    connection.autocommit = True
    record = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            record = cursor.fetchone()
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")
    return record
