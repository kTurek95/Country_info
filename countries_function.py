""" Module with all necessary function to run main module"""

import sqlite3
from matplotlib import pyplot as plt, ticker
import requests


def initialize(db_connection):
    """
    Initializes the 'Countries_and_capitals' table in a given SQLite database connection.

    Args:
        db_connection: An SQLite database connection.

    This function creates the table structure for storing information about countries, capitals, and populations.
    It does not return any value but commits the changes to the database.
    """
    table = '''CREATE TABLE Countries_and_capitals(
    query_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country VARCHAR,
    capital VARCHAR,
    population INTEGER
    )'''

    cursor = db_connection.cursor()
    cursor.execute(table)
    db_connection.commit()


def get_info_from_db(db_connection):
    """
    Retrieves country names and populations from the 'Countries_and_capitals' table in the database.

    Args:
        db_connection: An SQLite database connection.

    Returns:
        A list of tuples containing country names and populations.

    This function executes a SQL query to select the relevant data from the database
    and returns the retrieved rows as a list of tuples.
    """
    cursor = db_connection.cursor()
    result = cursor.execute(
        'SELECT country, population FROM Countries_and_capitals'
    )

    rows = result.fetchall()
    return rows


def save_country_and_capital(country: str) -> dict:
    """
    Retrieves information about a country from an online source and returns it as a dictionary.

    Args:
        country: The name of the country.

    Returns:
        A dictionary containing the country name, capital, and population (if found).

    This function makes an HTTP request to an online API to fetch information about the given country.
    It handles potential errors and returns the retrieved data in a dictionary format.
    """
    countries_capitals = {}
    response = requests.get('https://restcountries.com/v3.1/all')
    found = False

    try:
        for row in response.json():
            if row['name']['common'] == country:
                countries_capitals[country] = row['capital'][0]
                countries_capitals['Population'] = row['population']
                found = True
                break
            if row['name']['common'] != country:
                found = False
        if not found:
            raise ValueError('We don"t have such a country in our database.')

    except KeyError:
        print('The given country doesn"t have a capital.')
    except ValueError as message:
        print(message)
    except requests.exceptions.ConnectionError:
        print('There is no internet access')

    return countries_capitals


def add_country(db_connection, country: str):
    """
    Adds information about a country to the 'Countries_and_capitals' table in the database.

    Args:
        db_connection: An SQLite database connection.
        country: The name of the country to be added.

    This function adds a new record to the database with the country's name, capital, and population
    by calling the 'save_country_and_capital' function. It then commits the changes to the database.
    """
    countries_capitals = save_country_and_capital(country)

    for countries, cities in countries_capitals.items():
        if country == countries:
            capital = cities
    population = countries_capitals.get('Population')

    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO Countries_and_capitals'
                   '(country, capital, population) VALUES(?, ?, ?)',
                   (
                    country,
                    capital,
                    population
    ))

    db_connection.commit()


def check_if_country_in_db(db_connection, location: str, number: int):
    """
    Checks if a country with a specific capital and population exists in the database.

    Args:
        db_connection: An SQLite database connection.
        location: The capital of the country to be checked.
        number: The population of the country to be checked.

    Returns:
        A tuple containing the name of the country if found, or None if not found.

    This function executes a SQL query to search for a record matching the given capital and population
    in the 'Countries_and_capitals' table of the database and returns the result.
    """
    cursor = db_connection.cursor()
    result = cursor.execute(
        'SELECT country FROM Countries_and_capitals'
        ' WHERE capital=? AND population=?', (location, number)
    )

    return result.fetchone()


def give_chart():
    """
    Generates and displays a bar chart of country populations using data from the database.

    This function retrieves data from the 'Countries_and_capitals' table, creates a bar chart,
    and displays it using Matplotlib. It also handles formatting of the chart.
    """
    countries = []
    populations = []

    cursor = sqlite3.connect('Countries_and_capitals.db')
    results = get_info_from_db(cursor)

    for result in results:
        countries.append(result[0])
        populations.append(result[1])
    print(populations)

    plt.bar(countries, populations)

    formatter = ticker.EngFormatter()
    formatter.ENG_PREFIXES[-6] = 'm'

    if any(population > 100000000 for population in populations):
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(50000000))
    else:
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5000000))

    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('Populacja w danym kraju')
    plt.show()


def continent_table(db_connection):
    """
    Initializes the 'Continent_table' table in a given SQLite database connection.

    Args:
        db_connection: An SQLite database connection.

    This function creates the table structure for storing information about countries, continents, and languages.
    It does not return any value but commits the changes to the database.
    """
    table1 = '''CREATE TABLE Continent_table(
    query_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country VARCHAR,
    continent VARCHAR,
    country_language VARCHAR)'''

    cursor = db_connection.cursor()
    cursor.execute(table1)
    db_connection.commit()


def add_country_to_continent(db_connection):
    pass


# następna opcja w tym programie to stworzenie tabeli z kontynentami
# i połączenie jej z tabelą główną
# czyli jeżeli kraj o id 1 (hiszpania) w naszym api == europa
# to dodajemy ja do tabeli do kontynentu europa itd...
