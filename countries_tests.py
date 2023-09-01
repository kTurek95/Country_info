import sqlite3

from countries_function import get_info_from_db, check_if_country_in_db


def create_database():
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
    import os
    os.remove('information.db')


def test_get_info_from_db_test():
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
    create_database()
    db_connection = sqlite3.connect('information.db')

    remove_database()
    assert check_if_country_in_db(db_connection, 'Lisbon', 10305564) == ('Portugal',)
    assert check_if_country_in_db(db_connection, 'Tallin', 1331057) is None
