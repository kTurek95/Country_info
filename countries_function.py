from matplotlib import pyplot as plt, ticker
import sqlite3
import requests


def initialize(db_connection):
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
    cursor = db_connection.cursor()
    result = cursor.execute(
        'SELECT country, population FROM Countries_and_capitals'
    )

    rows = result.fetchall()
    return rows


def save_country_and_capital(country: str) -> dict:
    countries_capitals = dict()
    response = requests.get('https://restcountries.com/v3.1/all')
    found = False

    try:
        for row in response.json():
            if row['name']['common'] == country:
                countries_capitals[country] = row['capital'][0]
                countries_capitals['Population'] = row['population']
                found = True
                break
            elif row['name']['common'] != country:
                found = False
        if not found:
            raise ValueError('Nie mamy takiego państwa w bazie danych.')

    except KeyError:
        print('Podane państwo nie ma stolicy.')
    except ValueError as message:
        print(message)
    except requests.exceptions.ConnectionError:
        print('Nie ma dostępu do internetu')

    return countries_capitals


def add_country(db_connection, country: str):
    countries_capitals = save_country_and_capital(country)

    for countries, cities in countries_capitals.items():
        if country == countries:
            capital = cities
    population = countries_capitals.get('Population')

    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO Countries_and_capitals(country, capital, population) VALUES(?, ?, ?)', (
        country,
        capital,
        population
    ))

    db_connection.commit()


def check_if_country_in_db(db_connection, location: str, number: int):
    cursor = db_connection.cursor()
    result = cursor.execute(
        'SELECT country FROM Countries_and_capitals WHERE capital=? AND population=?', (location, number)
    )

    return result.fetchone()


def give_chart():
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
    table1 = '''CREATE TABLE Continent_table(
    query_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country VARCHAR,
    continent VARCHAR,
    country_language VARCHAR)'''

    cursor = db_connection.cursor()
    cursor.execute(table1)
    db_connection.commit()


def add_country_to_continent():
    pass

# następna opcja w tym programie to stworzenie tabeli z kontynentami i połączenie jej z tabelą główną
# czyli jeżeli kraj o id 1 (hiszpania) w naszym api == europa to dodajemy ja do tabeli do kontynentu europa itd...