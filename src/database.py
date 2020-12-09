import sqlite3
import requests
import json
from datetime import datetime


def create_databases():
    print("Connecting to database...")

    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    print("Database connected!")

    print("Creating tables...")

    query = '''CREATE TABLE IF NOT EXISTS Global(id INTEGER PRIMARY KEY, Date TEXT, TotalConfirmed INTEGER, TotalDeaths INTEGER, TotalRecovered INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS Countries(id INTEGER PRIMARY KEY, Country TEXT, date_id REFERENCES Global(id), TotalConfirmed INTEGER, TotalDeaths INTEGER, TotalRecovered INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS CountriesGender(id INTEGER PRIMARY KEY, Country TEXT, Date TEXT, country_id REFERENCES Countries(id), MaleCases INTEGER, FemaleCases INTEGER, TotalCases INTEGER, MaleDeaths INTEGER, FemaleDeaths INTEGER, TotalDeaths INTEGER, MalePop INTEGER, FemalePop INTEGER, TotalPop INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS USA(id INTEGER PRIMARY KEY, date TEXT, Confirmed INTEGER, Negative INTEGER, Deaths INTEGER, Recovered INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS States(id INTEGER PRIMARY KEY, date TEXT, State TEXT, date_id REFERENCES USA(id), Confirmed INTEGER, Negative INTEGER, Deaths INTEGER, Recovered INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS USAGender (id INTEGER PRIMARY KEY, Date TEXT, State TEXT, Sex TEXT, AgeGroup TEXT, COVID19Deaths INTEGER, PneumoniaDeaths INTEGER, InfluenzaDeaths INTEGER, PneumoniaAndCOVID19Deaths INTEGER, PneumoniaInfluenzaORCOVID19Deaths INTEGER, TotalDeaths INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS USAStateGender(id INTEGER PRIMARY KEY, Date TEXT, State TEXT, state_id REFERENCES States(id), date_id REFERENCES USAGender(Date), Sex TEXT, AgeGroup TEXT, COVID19Deaths INTEGER, PneumoniaDeaths INTEGER, InfluenzaDeaths INTEGER, PneumoniaAndCOVID19Deaths INTEGER, PneumoniaInfluenzaORCOVID19Deaths INTEGER, TotalDeaths INTEGER);'''
    c.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS CountriesAgeSex(id INTEGER PRIMARY KEY, Date TEXT, Country TEXT, country_id REFERENCES CountriesGender(id), AgeGroup TEXT, FemaleDeaths INTEGER, MaleDeaths INTEGER);'''
    c.execute(query)

    print("Tables created!")


def retrieve_data(url):
    """retrieves data from API

    Args:
        url (string): the url for the API

    Returns:
        dictionary: JSON data as a dictionary
    """
    res = requests.get(url)
    return json.loads(res.text)


def save_usa_data():
    """this function specifically saves USA COVID data into a single row table
    """
    url = 'https://api.covidtracking.com/v1/us/current.json'
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    data = retrieve_data(url)[0]
    date = datetime.today().strftime('%Y-%m-%d')

    query = "INSERT INTO USA(date, Confirmed, Negative, Deaths, Recovered) VALUES (?, ?, ?, ?, ?);"
    c.execute(query, (date, data['positive'],
                      data['negative'], data['death'], data['recovered']))

    conn.commit()
    conn.close()


def save_usa_state_data():
    """this function saves specific USA state COVID data into a multi-row table
    """
    url = 'https://api.covidtracking.com/v1/states/current.json'
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    data = retrieve_data(url)
    date = datetime.today().strftime('%Y-%m-%d')

    data = sorted(data, key=lambda x: x['positive'], reverse=True)

    query = "SELECT date, id FROM USA"
    c.execute(query)
    check = len(c.fetchall())
    c.execute(query)
    ref = c.fetchall()
    ref_dict = dict(ref)

    query = "SELECT * FROM States;"
    c.execute(query)

    count = len(c.fetchall())

    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    us_states = {y: x for x, y in us_state_abbrev.items()}

    if check > 0:
        if count < 56:
            if count == 0:
                for i in data[:25]:
                    date_id = ref_dict[date]
                    state = us_states[i['state']]
                    query = "INSERT INTO States(date, state, date_id, Confirmed, Negative, Deaths, Recovered) VALUES (?, ?, ?, ?, ?, ?, ?);"
                    c.execute(
                        query, (date, state, date_id, i['positive'], i['negative'], i['death'], i['recovered']))
            elif count == 25:
                for i in data[25:50]:
                    date_id = ref_dict[date]
                    state = us_states[i['state']]
                    query = "INSERT INTO States(date, state, date_id, Confirmed, Negative, Deaths, Recovered) VALUES (?, ?, ?, ?, ?, ?, ?);"
                    c.execute(
                        query, (date, state, date_id, i['positive'], i['negative'], i['death'], i['recovered']))
            elif count == 50:
                for i in data[50:]:
                    date_id = ref_dict[date]
                    state = us_states[i['state']]
                    query = "INSERT INTO States(date, state, date_id, Confirmed, Negative, Deaths, Recovered) VALUES (?, ?, ?, ?, ?, ?, ?);"
                    c.execute(
                        query, (date, state, date_id, i['positive'], i['negative'], i['death'], i['recovered']))
        elif count < 112:
            if count == 56:
                for i in data[:25]:
                    date_id = ref_dict[date]
                    state = us_states[i['state']]
                    query = "INSERT INTO States(date, state, date_id, Confirmed, Negative, Deaths, Recovered) VALUES (?, ?, ?, ?, ?, ?, ?);"
                    c.execute(
                        query, (date, state, date_id, i['positive'], i['negative'], i['death'], i['recovered']))
            if count == 81:
                for i in data[25:50]:
                    date_id = ref_dict[date]
                    state = us_states[i['state']]
                    query = "INSERT INTO States(date, state, date_id, Confirmed, Negative, Deaths, Recovered) VALUES (?, ?, ?, ?, ?, ?, ?);"
                    c.execute(
                        query, (date, state, date_id, i['positive'], i['negative'], i['death'], i['recovered']))
            if count == 106:
                for i in data[50:]:
                    date_id = ref_dict[date]
                    state = us_states[i['state']]
                    query = "INSERT INTO States(date, state, date_id, Confirmed, Negative, Deaths, Recovered) VALUES (?, ?, ?, ?, ?, ?, ?);"
                    c.execute(
                        query, (date, state, date_id, i['positive'], i['negative'], i['death'], i['recovered']))
    else:
        print("Waiting for USA data to be filled")

    conn.commit()
    conn.close()


def save_usa_gender_data():
    """this function populates gender COVID data for the entire United States along with comparisons to other illnesses
    """
    conn = sqlite3.connect('covid.db')
    c = conn.cursor()

    data_all = retrieve_data(
        'https://data.cdc.gov/resource/9bhg-hcku.json?state=United%20States')
    date = datetime.today().strftime('%Y-%m-%d')

    query = '''SELECT * FROM USAGender;'''
    c.execute(query)
    count = len(c.fetchall())

    if count < 64:
        if count == 0:
            for data in data_all[:25]:
                query = '''INSERT INTO USAGender(Date, State, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                c.execute(query, (date, data['state'], data['sex'], data['age_group_new'], data['covid_19_deaths'],
                                  data['pneumonia_deaths'], data['influenza_deaths'], data['pneumonia_and_covid_19_deaths'], data['pneumonia_influenza_or_covid'], data['total_deaths']))
        if count == 25:
            for data in data_all[25:50]:
                query = '''INSERT INTO USAGender(Date, State, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                c.execute(query, (date, data['state'], data['sex'], data['age_group_new'], data['covid_19_deaths'],
                                  data['pneumonia_deaths'], data['influenza_deaths'], data['pneumonia_and_covid_19_deaths'], data['pneumonia_influenza_or_covid'], data['total_deaths']))
        if count == 50:
            for data in data_all[50:]:
                query = '''INSERT INTO USAGender(Date, State, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                c.execute(query, (date, data['state'], data['sex'], data['age_group_new'], data['covid_19_deaths'],
                                  data['pneumonia_deaths'], data['influenza_deaths'], data['pneumonia_and_covid_19_deaths'], data['pneumonia_influenza_or_covid'], data['total_deaths']))
    conn.commit()
    conn.close()


def save_usa_state_gender_data():
    """this function saves Gender COVID data for every individual US State as well as the territories
    """
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    state_data = []
    date = datetime.today().strftime('%Y-%m-%d')

    state_names = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi",
                   "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

    for state in state_names:
        data = retrieve_data(
            f'https://data.cdc.gov/resource/9bhg-hcku.json?state={state}&age_group_new=All%20Ages')
        state_data.append(data)

    query = '''SELECT * FROM USAStateGender;'''
    c.execute(query)
    count = len(c.fetchall())

    query = '''SELECT State, id FROM States;'''
    c.execute(query)
    state_track = len(c.fetchall())
    c.execute(query)
    ref = c.fetchall()
    state_ref = dict(ref)

    query = '''SELECT Date, id FROM USAGender;'''
    c.execute(query)
    usagender_track = len(c.fetchall())
    c.execute(query)
    ref = c.fetchall()
    date_ref = dict(ref)

    if state_track == 56 and usagender_track == 64:
        states = sum(state_data, [])
        if count < 200:
            if count == 0:
                for state in states[:25]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    if 'influenza_deaths' not in state:
                        state['influenza_deaths'] = ''
                    if 'total_deaths' not in state:
                        state['total_deaths'] = ''
                    if 'pneumonia_deaths' not in state:
                        state['pneumonia_deaths'] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
            if count == 25:
                for state in states[25:50]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    if 'influenza_deaths' not in state:
                        state['influenza_deaths'] = ''
                    if 'total_deaths' not in state:
                        state['total_deaths'] = ''
                    if 'pneumonia_deaths' not in state:
                        state['pneumonia_deaths'] = ''
                    if 'pneumonia_influenza_or_covid' not in state:
                        state['pneumonia_influenza_or_covid'] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
            if count == 50:
                for state in states[50:75]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    params = ['total_deaths', 'covid_19_deaths', 'pneumonia_deaths', 'influenza_deaths',
                            'pneumonia_and_covid_19_deaths', 'pneumonia_influenza_or_covid']
                    for param in params:
                        if param not in state:
                            state[param] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
            if count == 75:
                for state in states[75:100]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    params = ['total_deaths', 'covid_19_deaths', 'pneumonia_deaths', 'influenza_deaths',
                            'pneumonia_and_covid_19_deaths', 'pneumonia_influenza_or_covid']
                    for param in params:
                        if param not in state:
                            state[param] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
            if count == 100:
                for state in states[100:125]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    params = ['total_deaths', 'covid_19_deaths', 'pneumonia_deaths', 'influenza_deaths',
                            'pneumonia_and_covid_19_deaths', 'pneumonia_influenza_or_covid']
                    for param in params:
                        if param not in state:
                            state[param] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
            if count == 125:
                for state in states[125:150]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    params = ['total_deaths', 'covid_19_deaths', 'pneumonia_deaths', 'influenza_deaths',
                            'pneumonia_and_covid_19_deaths', 'pneumonia_influenza_or_covid']
                    for param in params:
                        if param not in state:
                            state[param] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
            if count == 150:
                for state in states[150:175]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    params = ['total_deaths', 'covid_19_deaths', 'pneumonia_deaths', 'influenza_deaths',
                            'pneumonia_and_covid_19_deaths', 'pneumonia_influenza_or_covid']
                    for param in params:
                        if param not in state:
                            state[param] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
            if count == 175:
                for state in states[175:]:
                    state_id = state_ref[state['state']]
                    date_id = date_ref[date]
                    params = ['total_deaths', 'covid_19_deaths', 'pneumonia_deaths', 'influenza_deaths',
                            'pneumonia_and_covid_19_deaths', 'pneumonia_influenza_or_covid']
                    for param in params:
                        if param not in state:
                            state[param] = ''
                    query = '''INSERT INTO USAStateGender(Date, State, state_id, date_id, Sex, AgeGroup, COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, PneumoniaAndCOVID19Deaths, PneumoniaInfluenzaORCOVID19Deaths, TotalDeaths) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (date, state['state'], state_id, date_id, state['sex'], state['age_group_new'], state['covid_19_deaths'], state['total_deaths'],
                                    state['pneumonia_deaths'], state['influenza_deaths'], state['pneumonia_and_covid_19_deaths'], state['pneumonia_influenza_or_covid']))
    else:
        print("Waiting for States and USAGender tables to be filled!")

    conn.commit()
    conn.close()


def save_countries_age_gender():
    """this function saves gender data on multiple countries around the world, in particular COVID deaths by country, and also the age groups of the deaths. Note that not every country has offered data on this
    """
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    data = retrieve_data(
        'https://api.globalhealth5050.org/api/v1/agesex')['data']

    query = '''SELECT Country FROM CountriesGender'''
    c.execute(query)
    countries = c.fetchall()

    count = []

    query = '''SELECT Country, id FROM CountriesGender;'''
    c.execute(query)
    track = len(c.fetchall())
    c.execute(query)
    ref_country = dict(c.fetchall())

    query = '''SELECT * FROM CountriesAgeSex;'''
    c.execute(query)
    number = len(c.fetchall())

    # print(data['data']['Afghanistan']['DeathsbyAgeSex'])
    for country in countries:
        try:
            if country[0] not in data:
                pass
            else:
                # print(country[0])
                count.append(data[country[0]]['DeathsbyAgeSex'])
        except KeyError as e:
            pass
    count = sum(count, [])

    if track == 115:
        if number < 409:
            if number == 0:
                for i in count[:25]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 25:
                for i in count[25:50]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 50:
                for i in count[50:75]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 75:
                for i in count[75:100]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 100:
                for i in count[100:125]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 125:
                for i in count[125:150]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 150:
                for i in count[150:175]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 175:
                for i in count[175:200]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 200:
                for i in count[200:225]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 225:
                for i in count[225:250]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 250:
                for i in count[250:275]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 275:
                for i in count[275:300]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 300:
                for i in count[300:325]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 325:
                for i in count[325:350]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 350:
                for i in count[350:375]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 375:
                for i in count[375:400]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
            if number == 400:
                for i in count[400:]:
                    country_id = ref_country[i['country']]
                    query = '''INSERT INTO CountriesAgeSex(Date, Country, country_id, AgeGroup, FemaleDeaths, MaleDeaths) VALUES (?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (i['date'], i['country'], country_id,
                                    i['age_group'], i['deathsF'], i['deathsM']))
    else:
        print("Waiting for CountriesGender table to be filled!")

    conn.commit()
    conn.close()


def save_global_data():
    """this function inserts current global COVID data in total
    """
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    data = retrieve_data('https://api.covid19api.com/summary')['Global']
    date = datetime.today().strftime('%Y-%m-%d')

    query = '''SELECT * FROM Global;'''
    c.execute(query)
    count = len(c.fetchall())

    if count < 1:
        query = '''INSERT INTO Global(Date, TotalConfirmed, TotalDeaths, TotalRecovered) VALUES (?, ?, ?, ?);'''
        c.execute(query, (date, data['TotalConfirmed'],
                          data['TotalDeaths'], data['TotalRecovered']))

    conn.commit()
    conn.close()


def save_country_data():
    """
    this function saves current COVID data on individual countries that offer that data
    """
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


def save_countries_gender():
    """this function saves saves general COVID gender deaths for every country, rather than age groups
    """
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    data = []

    data = retrieve_data(
        'https://api.globalhealth5050.org/api/v1/summary')['data']

    query = '''SELECT country, id FROM Countries;'''
    c.execute(query)
    check = len(c.fetchall())
    c.execute(query)
    ref = c.fetchall()
    ref = dict(ref)

    query = '''SELECT * FROM CountriesGender;'''
    c.execute(query)
    count = len(c.fetchall())

    data = [v for v in data.values()]

    if check == 150:
        if count < 150:
            if count == 0:
                for v in data[:25]:
                    # if v['MaleCases'] == '' or v['FemaleCases'] == '' or v['TotalCases'] == '' or v['MaleDeaths'] == '' or v['FemaleDeaths'] == '' or v['TotalDeaths'] == '':
                    #     pass
                    try:
                        country_id = ref[v['country']]
                    except KeyError as e:
                        continue
                    query = '''INSERT INTO CountriesGender(Country, Date, country_id, MaleCases, FemaleCases, TotalCases, MaleDeaths, FemaleDeaths, TotalDeaths, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (v['country'], v['date'], country_id,
                                      v['cases_male'], v['cases_female'], v['cases_total'], v['deaths_male'], v['deaths_female'], v['deaths_total'], v['malepop2020'], v['femalepop2020'], v['totpop2020']))
            if count == 22:
                for v in data[25:50]:
                    try:
                        country_id = ref[v['country']]
                    except KeyError as e:
                        continue
                    query = '''INSERT INTO CountriesGender(Country, Date, country_id, MaleCases, FemaleCases, TotalCases, MaleDeaths, FemaleDeaths, TotalDeaths, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (v['country'], v['date'], country_id,
                                      v['cases_male'], v['cases_female'], v['cases_total'], v['deaths_male'], v['deaths_female'], v['deaths_total'], v['malepop2020'], v['femalepop2020'], v['totpop2020']))
            if count == 45:
                for v in data[50:75]:
                    try:
                        country_id = ref[v['country']]
                    except KeyError as e:
                        continue
                    query = '''INSERT INTO CountriesGender(Country, Date, country_id, MaleCases, FemaleCases, TotalCases, MaleDeaths, FemaleDeaths, TotalDeaths, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (v['country'], v['date'], country_id,
                                      v['cases_male'], v['cases_female'], v['cases_total'], v['deaths_male'], v['deaths_female'], v['deaths_total'], v['malepop2020'], v['femalepop2020'], v['totpop2020']))
            if count == 65:
                for v in data[75:100]:
                    try:
                        country_id = ref[v['country']]
                    except KeyError as e:
                        continue
                    query = '''INSERT INTO CountriesGender(Country, Date, country_id, MaleCases, FemaleCases, TotalCases, MaleDeaths, FemaleDeaths, TotalDeaths, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (v['country'], v['date'], country_id,
                                      v['cases_male'], v['cases_female'], v['cases_total'], v['deaths_male'], v['deaths_female'], v['deaths_total'], v['malepop2020'], v['femalepop2020'], v['totpop2020']))
            if count == 77:
                for v in data[100:125]:
                    try:
                        country_id = ref[v['country']]
                    except KeyError as e:
                        continue
                    query = '''INSERT INTO CountriesGender(Country, Date, country_id, MaleCases, FemaleCases, TotalCases, MaleDeaths, FemaleDeaths, TotalDeaths, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (v['country'], v['date'], country_id,
                                      v['cases_male'], v['cases_female'], v['cases_total'], v['deaths_male'], v['deaths_female'], v['deaths_total'], v['malepop2020'], v['femalepop2020'], v['totpop2020']))
            if count == 95:
                for v in data[125:150]:
                    try:
                        country_id = ref[v['country']]
                    except KeyError as e:
                        continue
                    query = '''INSERT INTO CountriesGender(Country, Date, country_id, MaleCases, FemaleCases, TotalCases, MaleDeaths, FemaleDeaths, TotalDeaths, MalePop, FemalePop, TotalPop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    c.execute(query, (v['country'], v['date'], country_id,
                                      v['cases_male'], v['cases_female'], v['cases_total'], v['deaths_male'], v['deaths_female'], v['deaths_total'], v['malepop2020'], v['femalepop2020'], v['totpop2020']))
    else:
        print("Waiting for Countries data to be filled!")
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

    query = "DROP TABLE USAGender"
    c.execute(query)

    query = "DROP TABLE USA;"
    c.execute(query)

    query = "DROP TABLE CountriesGender;"
    c.execute(query)

    conn.commit()
    conn.close()
