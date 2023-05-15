import sqlite3
from sys import argv
import countries_function

try:
    with sqlite3.connect('Countries_and_capitals.db') as connection:
        if len(argv) == 2 and argv[1] == 'setup':
            countries_function.initialize(connection)
except sqlite3.OperationalError:
    print('Tabela już istnieje')

while True:
    try:
        country = input('Podaj nazwę kraju: ')
        if country == 'koniec':
            countries_function.give_chart()
            break

        countries_dict = countries_function.save_country_and_capital(country)
        try:
            row = countries_function.check_if_country_in_db(connection, countries_dict[country], countries_dict['Population'])
            if row is None:
                try:
                    countries_function.add_country(connection, country)
                except UnboundLocalError:
                    pass
                print(f'Dodano {country} do bazy danych' )
            else:
                print(f'{country} jest już w bazie danych')
        except KeyError:
            pass
    except sqlite3.OperationalError:
        print('Nie posiadasz tabeli, do której możesz dodać dane')
        break



