""" Module with tests for countries_function module"""

import sqlite3
import os
from countries_function import get_info_from_db, check_if_country_in_db


def create_database():
    """
    Creates a SQLite database named 'information.db' if it does not already exist,
    and initializes a table 'Countries_and_capitals' to store information about countries,
    their capitals, and populations.
    Additionally, the function inserts sample data into the table to provide some initial data.
    """
    db_connection = sqlite3.connect('information.db')
    cursor = db_connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Countries_and_capitals(
        query_id INTEGER PRIMARY KEY AUTOINCREMENT,
        country VARCHAR,
        capital VARCHAR,
        population INTEGER
    )''')

    sample_data = [
        ('Poland', 'Warsaw', 37950802),
        ('Sweden', 'Stockholm', 10353442),
        ('Portugal', 'Lisbon', 10305564),
        ('France', 'Paris', 67391582),
        ('Italy', 'Rome', 59554023)
    ]

    cursor.executemany('INSERT INTO Countries_and_capitals'
                       '(country, capital, population)'
                       'VALUES (?, ?, ?)', sample_data,)

    db_connection.commit()
    db_connection.close()


def remove_database():
    """
    Removes the SQLite database file.
    """
    os.remove('information.db')


def test_get_info_from_db_test():
    """
    This test function verifies the functionality of the
    'get_info_from_db' function by performing the following steps:
    1. Creates a test database using 'create_database'.
    2. Retrieves information from the test database using 'get_info_from_db'.
    3. Compares the retrieved data with the expected data.
    4. Removes the test database after the test is complete.

    The expected returns are a list of tuples containing country names and populations.
    """
    create_database()
    db_connection = sqlite3.connect('information.db')
    fetched_data = get_info_from_db(db_connection)
    expected_returns = [
        ('Poland', 37950802),
        ('Sweden', 10353442),
        ('Portugal', 10305564),
        ('France', 67391582),
        ('Italy', 59554023)
    ]

    remove_database()
    assert fetched_data == expected_returns
    assert len(fetched_data) == 5


def test_check_if_country_in_db():
    """
    This test function verifies the functionality of the
    'check_if_country_in_db' function by performing the following steps:
    1. Creates a test database using 'create_database'.
    2. Attempts to check if specific countries and populations are present in the test database.
    3. Compares the results with expected outcomes.
    4. Removes the test database after the test is complete.

    The expected outcomes include matching records
    if the country and population exist in the database,
    and None if the record does not exist.
    """
    create_database()
    db_connection = sqlite3.connect('information.db')

    remove_database()
    assert check_if_country_in_db(db_connection, 'Lisbon', 10305564) == ('Portugal',)
    assert check_if_country_in_db(db_connection, 'Tallin', 1331057) is None
