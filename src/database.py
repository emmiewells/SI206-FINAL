import sqlite3
import requests
import json
from datetime import datetime


def create_databases():
    print("Creating databases...")

    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    query = '''CREATE TABLE IF NOT EXISTS Global(id INTEGER PRIMARY KEY, Date TEXT, TotalConfirmed INTEGER, TotalDeaths INTEGER, TotalRecovered INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS Countries(id INTEGER PRIMARY KEY, Country TEXT, date_id REFERENCES Global(id), TotalConfirmed INTEGER, TotalDeaths INTEGER, TotalRecovered INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS CountriesGenderCases(id INTEGER PRIMARY KEY, Country TEXT, Date TEXT, country_id REFERENCES Countries(id), MaleCases INTEGER, FemaleCases INTEGER, TotalCases INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS CountriesGenderDeaths(id INTEGER PRIMARY KEY, Country TEXT, Date TEXT, country_id REFERENCES CountriesGenderCases(id), MaleDeaths INTEGER, FemaleDeaths INTEGER, TotalDeaths INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS CountriesGenderPopulation(id INTEGER PRIMARY KEY, Country TEXT, Date TEXT, country_id REFERENCES CountriesGenderCases(id), MalePop INTEGER, FemalePop INTEGER, TotalPop INTEGER);'''
    c.execute(query)

    print("Databases created!")


def retrieve_data(url):
    res = requests.get(url)
    return json.loads(res.text)


def save_global_data():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    data = retrieve_data('https://api.covid19api.com/summary')['Global']
    date = datetime.today().strftime('%Y-%m-%d')

    query = '''SELECT * FROM Global'''
    c.execute(query)
    count = len(c.fetchall())

    if count < 1:
        query = '''INSERT INTO Global(Date, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?, ?, ?, ?);'''
        c.execute(query, (date, data['TotalConfirmed'],
                          data['TotalDeaths'], data['TotalRecovered']))

    conn.commit()
    conn.close()


def save_country_data():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    data = retrieve_data('https://api.covid19api.com/summary')['Countries']
    date = datetime.today().strftime('%Y-%m-%d')

    for i in data:
        if i['Country'] == "Korea (South)":
            i['Country'] = "South Korea"
        elif i['Country'] == "Iran, Islamic Republic of":
            i['Country'] = 'Iran'
        elif i['Country'] == 'Congo (Brazzaville)':
            del i
        elif i['Country'] == 'Congo (Kinshasa)':
            i['Country'] = "Congo"

    data = sorted(data, key=lambda x: x['TotalConfirmed'], reverse=True)

    query = '''SELECT * FROM Countries'''
    c.execute(query)
    count = len(c.fetchall())

    query = '''SELECT Date, id FROM Global'''
    c.execute(query)
    ref = c.fetchall()
    ref_dict = dict(ref)

    if count < 150:
        if count == 0:
            for i in data[:25]:
                date_id = ref_dict[date]
                query = '''INSERT INTO Countries(Country, date_id, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?,?, ?, ?, ?);'''
                c.execute(query, (i['Country'], date_id, i['TotalConfirmed'],
                                  i['TotalDeaths'], i['TotalRecovered']))
        if count == 25:
            for i in data[25:50]:
                date_id = ref_dict[date]
                query = '''INSERT INTO Countries(Country, date_id, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?, ?, ?, ?, ?);'''
                c.execute(query, (i['Country'], date_id, i['TotalConfirmed'],
                                  i['TotalDeaths'], i['TotalRecovered']))
        if count == 50:
            for i in data[50:75]:
                date_id = ref_dict[date]
                query = '''INSERT INTO Countries(Country, date_id, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?, ?, ?, ?, ?);'''
                c.execute(query, (i['Country'], date_id, i['TotalConfirmed'],
                                  i['TotalDeaths'], i['TotalRecovered']))
        if count == 75:
            for i in data[75:100]:
                date_id = ref_dict[date]
                query = '''INSERT INTO Countries(Country, date_id, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?, ?, ?, ?, ?);'''
                c.execute(query, (i['Country'], date_id, i['TotalConfirmed'],
                                  i['TotalDeaths'], i['TotalRecovered']))
        if count == 100:
            for i in data[100:125]:
                date_id = ref_dict[date]
                query = '''INSERT INTO Countries(Country, date_id, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?, ?, ?, ?, ?);'''
                c.execute(query, (i['Country'], date_id, i['TotalConfirmed'],
                                  i['TotalDeaths'], i['TotalRecovered']))
        if count == 125:
            for i in data[125:150]:
                date_id = ref_dict[date]
                query = '''INSERT INTO Countries(Country, date_id, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?, ?, ?, ?, ?);'''
                c.execute(query, (i['Country'], date_id, i['TotalConfirmed'],
                                  i['TotalDeaths'], i['TotalRecovered']))

    conn.commit()
    conn.close()


def save_countries_gender_cases():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    data = []

    data = retrieve_data(
        'https://api.globalhealth5050.org/api/v1/summary')['data']

    query = '''SELECT country, id FROM Countries;'''
    c.execute(query)
    ref = c.fetchall()
    ref = dict(ref)

    query = '''SELECT * FROM CountriesGenderCases;'''
    c.execute(query)
    count = len(c.fetchall())

    data = [v for v in data.values()]

    if count < 150:
        if count == 0:
            for v in data[:25]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderCases(Country, Date, country_id, MaleCases, FemaleCases, TotalCases) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['cases_male'], v['cases_female'], v['cases_total']))
        if count == 22:
            for v in data[25:50]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderCases(Country, Date, country_id, MaleCases, FemaleCases, TotalCases) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['cases_male'], v['cases_female'], v['cases_total']))
        if count == 45:
            for v in data[50:75]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderCases(Country, Date, country_id, MaleCases, FemaleCases, TotalCases) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['cases_male'], v['cases_female'], v['cases_total']))
        if count == 65:
            for v in data[75:100]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderCases(Country, Date, country_id, MaleCases, FemaleCases, TotalCases) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['cases_male'], v['cases_female'], v['cases_total']))
        if count == 77:
            for v in data[100:125]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderCases(Country, Date, country_id, MaleCases, FemaleCases, TotalCases) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['cases_male'], v['cases_female'], v['cases_total']))
        if count == 95:
            for v in data[125:150]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderCases(Country, Date, country_id, MaleCases, FemaleCases, TotalCases) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['cases_male'], v['cases_female'], v['cases_total']))
    conn.commit()
    conn.close()


def save_countries_gender_deaths():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    data = []

    data = retrieve_data(
        'https://api.globalhealth5050.org/api/v1/summary')['data']

    query = '''SELECT country, id FROM CountriesGenderCases;'''
    c.execute(query)
    ref = c.fetchall()
    ref = dict(ref)

    query = '''SELECT * FROM CountriesGenderDeaths;'''
    c.execute(query)
    count = len(c.fetchall())

    data = [v for v in data.values()]

    if count < 150:
        if count == 0:
            for v in data[:25]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderDeaths(Country, Date, country_id, MaleDeaths, FemaleDeaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 22:
            for v in data[25:50]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderDeaths(Country, Date, country_id, MaleDeaths, FemaleDeaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 45:
            for v in data[50:75]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderDeaths(Country, Date, country_id, MaleDeaths, FemaleDeaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 65:
            for v in data[75:100]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderDeaths(Country, Date, country_id, MaleDeaths, FemaleDeaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 77:
            for v in data[100:125]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderDeaths(Country, Date, country_id, MaleDeaths, FemaleDeaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 95:
            for v in data[125:150]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderDeaths(Country, Date, country_id, MaleDeaths, FemaleDeaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        conn.commit()
        conn.close()


def save_countries_gender_total():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    data = retrieve_data(
        'https://api.globalhealth5050.org/api/v1/summary')['data']

    query = '''SELECT country, id FROM CountriesGenderCases;'''
    c.execute(query)
    ref = c.fetchall()
    ref = dict(ref)

    query = '''SELECT * FROM CountriesGenderPopulation;'''
    c.execute(query)
    count = len(c.fetchall())

    data = [v for v in data.values()]

    if count < 150:
        if count == 0:
            for v in data[:25]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderPopulation(Country, Date, country_id, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 22:
            for v in data[25:50]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderPopulation(Country, Date, country_id, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 45:
            for v in data[50:75]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderPopulation(Country, Date, country_id, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 65:
            for v in data[75:100]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderPopulation(Country, Date, country_id, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 77:
            for v in data[100:125]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderPopulation(Country, Date, country_id, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        elif count == 95:
            for v in data[125:150]:
                try:
                    country_id = ref[v['country']]
                except KeyError as e:
                    continue
                query = '''INSERT INTO CountriesGenderPopulation(Country, Date, country_id, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?);'''
                c.execute(query, (v['country'], v['date'], country_id,
                                  v['deaths_male'], v['deaths_female'], v['deaths_total']))
        conn.commit()
        conn.close()


def delete_rows(table, rows):
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    query = f"DELETE FROM {table} WHERE ID > {rows};"
    c.execute(query)

    print("Rows deleted!")

    conn.commit()
    conn.close()


def start_over():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    query = "DROP TABLE Countries;"
    c.execute(query)

    query = "DROP TABLE Global;"
    c.execute(query)

    query = "DROP TABLE CountriesGenderCases;"
    c.execute(query)

    query = "DROP TABLE CountriesGenderDeaths;"
    c.execute(query)

    query = "DROP TABLE CountriesGenderPopulation;"
    c.execute(query)

    conn.commit()
    conn.close()
