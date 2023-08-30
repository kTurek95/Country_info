import sqlite3
from sys import argv

from countries_function import initialize, continent_table, give_chart, save_country_and_capital, \
    check_if_country_in_db, add_country


def main():
    try:
        with sqlite3.connect('Countries_and_capitals.db') as connection:
            if len(argv) == 2 and argv[1] == 'setup':
                initialize(connection)
                with sqlite3.connect('Continent_table.db') as connection1:
                    continent_table(connection1)
    except sqlite3.OperationalError:
        print('Table is already exist')

    while True:
        try:
            country = input('Enter the name of the country or type "end" to finish: ')
            if country == 'end':
                give_chart()
                break
            countries_dict = save_country_and_capital(country)
            try:
                row = check_if_country_in_db(connection, countries_dict[country], countries_dict['Population'])
                if row is None:
                    try:
                        add_country(connection, country)
                    except UnboundLocalError:
                        pass
                    print(f'Added {country} to database')
                else:
                    print(f'{country} is already in the database')
            except KeyError:
                pass
        except sqlite3.OperationalError:
            print('You do not have a table to which you can add data')
            break


if __name__ == '__main__':
    main()
