import sqlite3


# average amount of males that have died from covid 
# average amount of females that have died from covid



# # a dummy test function for writing data to file
# def test():
#     print("Hello, calculate!")

#     conn = sqlite3.connect("covid.db")
#     c = conn.cursor()

#     query = '''SELECT * FROM Global;'''
#     c.execute(query)

#     global_data = c.fetchone()

#     query = '''SELECT * FROM Countries;'''
#     c.execute(query)

#     country_data = c.fetchall()
#     print(country_data)

#     with open("test.txt", "w") as file:
#         for i in country_data:
#             file.write(f"The country is {i[1]}")


# this makes calculations using the Countries and Global tables
def calculate_global_data():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    # fetching data
    query = '''SELECT MAX(Countries.TotalConfirmed), MAX(Countries.TotalDeaths), MAX(Countries.TotalRecovered), Global.TotalConfirmed, Global.TotalDeaths, Global.TotalRecovered FROM Countries JOIN Global ON Global.id = Countries.date_id;'''
    c.execute(query)
    data = c.fetchone()

    print(data[0])  # highest number of cases

    query = f'''SELECT Country FROM Countries WHERE TotalConfirmed = {data[0]};'''
    c.execute(query)
    confirmed_country = c.fetchone()[0]
    print(confirmed_country)

    print(data[1])  # highest number of deaths

    query = f'''SELECT Country FROM Countries WHERE TotalDeaths = {data[1]};'''
    c.execute(query)
    deaths_country = c.fetchone()[0]
    print(deaths_country)

    print(data[2])

    query = f'''SELECT Country FROM Countries WHERE TotalRecovered = {data[2]};'''
    c.execute(query)
    recovered_country = c.fetchone()[0]
    print(recovered_country)

    # calculating data
    percentage_confirmed = int(round(data[0] / data[3], 2) * 100)
    print(percentage_confirmed)

    percentage_death = int(round(data[1] / data[4], 2) * 100)
    print(percentage_death)

    percentage_recovered = int(round(data[2] / data[5], 2) * 100)
    print(percentage_recovered)

    # formatting strings
    confirmed = f'{data[0]:,}'
    deaths = f'{data[1]:,}'
    recovered = f'{data[2]:,}'

    # writing to file
    with open("covid.txt", "w") as file:
        file.write("### Global COVID Calculations ###")
        file.write(
            f"\nThe country with the highest COVID case count is {confirmed_country}, with a total case count of {confirmed}, accounting for about {percentage_confirmed}% of all cases in the world!\n\n")

        file.write(
            f"The country with the highest COVID death count is {deaths_country}, with a total death count of {deaths}, accounting for {percentage_death}% of all death.s\n\n")

        file.write(
            f"The country with the highest COVID recovery count is {recovered_country}, with a total recovery count of {recovered}, accounting for {percentage_recovered}% of all recoveries in the world!\n\n")


# # this will be used to calculate the States and USA tables
def calculate_usa_data():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    # fetching data
    query = '''SELECT MAX(States.Confirmed), MAX(States.Negative), MAX(States.Deaths), MAX(States.Recovered), USA.Confirmed, USA.Negative, USA.Deaths, USA.Recovered FROM States JOIN USA ON States.date_id = USA.id;'''
    c.execute(query)
    data = c.fetchone()

    query = f'''SELECT State FROM States WHERE Confirmed = {data[0]};'''
    c.execute(query)
    confirmed_state = c.fetchone()[0]

    query = f'''SELECT State FROM States WHERE Negative = {data[1]};'''
    c.execute(query)
    negative_state = c.fetchone()[0]

    query = f'''SELECT State FROM States WHERE Deaths = {data[2]};'''
    c.execute(query)
    deaths_state = c.fetchone()[0]

    query = f'''SELECT State FROM States WHERE Recovered = {data[3]};'''
    c.execute(query)
    recovered_state = c.fetchone()[0]

    # percentage calculation
    percentage_confirmed = int(round(data[0] / data[4], 2) * 100)
    percentage_negative = int(round(data[1] / data[5], 2) * 100)
    percentage_deaths = int(round(data[2] / data[6], 2) * 100)
    percentage_recovered = int(round(data[3] / data[7], 2) * 100)

    # format strings
    confirmed = f'{data[0]:,}'
    negative = f'{data[1]:,}'
    deaths = f'{data[2]:,}'
    recovered = f'{data[3]:,}'

    # writing to file
    with open("covid.txt", "a") as file:
        file.write("### US State COVID Calculations ###\n\n")
        file.write(
            f"Out of all of the US States, the state with the highest COVID cases is {confirmed_state} with {confirmed} cases, which make up about {percentage_confirmed}% of all cases countrywide.\n\n")
        file.write(
            f"Thus far, the deadliest US state is {deaths_state} with {deaths} deaths, which account for {percentage_deaths}% of all deaths.\n\n")
        file.write(
            f"But on the lighter side, the state with the most amount of recoveries is {recovered_state} with {recovered} total recovered and {percentage_recovered}% of all recoveries!\n\n")


# # this will be used to make calculations using the some of the gender tables (TBD)
# #def calculate_gender_data():
# #    calculate_global_data()  # these will run within
#     # calculate_usa_data()

#     # conn = sqlite3.connect("covid.db")
#     # c = conn.cursor()

#     # print("Calculating gender data...")
    
    
    
    
    
#     # query = '''SELECT USAGender.Date, USAGender.State, USAGender.Sex, USAGender.AgeGroup, USAGender.COVID19Deaths, USAStateGender.State, USAStateGender.Sex, USAStateGender.AgeGroup, USAStateGender.COVID19Deaths FROM USAGender JOIN USAStateGender ON USAStateGender.date_id = USAGender.id;'''
#     # c.execute(query)
    
#     # data = c.fetchall()
    
#     # dates = [i[0] for i in data]
#     # states = [i[1] for i in data]
#     # sex = [i[2] for i in data]
#     # print(sex)
    
#     # finding countries with highest male counts and female counts
#     query = '''SELECT Countries.Country, CountriesGender.MaleDeaths, CountriesGender.FemaleDeaths, CountriesGender.TotalDeaths FROM CountriesGender JOIN Countries ON Countries.id = CountriesGender.country_id;'''
#     c.execute(query)
    
#     data = c.fetchall()
#     # get rid of empty data
#     for i in data:
#         if i[1] == '':
#             data.remove(i)
    
    
#     # print(data)
#     countries = [i[0] for i in data]
#     male_deaths = [i[1] for i in data]
#     female_deaths = [i[2] for i in data]
#     total_deaths = [i[3] for i in data]
#     while '' in male_deaths:
#         male_deaths.remove('')
#         female_deaths.remove('')
#         total_deaths.remove('')
#     # print(male_deaths)
#     # print(female_deaths)
#     # print(total_deaths)
#     if '' in total_deaths:
#         total_deaths.remove('')
        
#     male_deaths = sorted(male_deaths, reverse=True)
#     print(male_deaths)
    
#     query = f'''SELECT id, Country from CountriesGender WHERE MaleDeaths = {male_deaths[0]};'''
#     c.execute(query)
    
#     male_death_country = c.fetchall()[0][1]
    
#     female_deaths = sorted(female_deaths, reverse=True)
#     print(female_deaths)

#     query = f'''SELECT id, Country from CountriesGender WHERE FemaleDeaths = {female_deaths[0]};'''
#     c.execute(query)

#     female_death_country = c.fetchall()
    
    # for men in mexico, men account for 
    # query = f'''SELECT TotalDeaths FROM CountriesGender WHERE Country = '{male_death_country}';'''
    # print(c.fetchall())


def calculate_usa_gender_data():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    
    query = '''SELECT USAGender.Date, USAGender.State, USAStateGender.State, USAStateGender.state_id, USAStateGender.COVID19Deaths FROM USAGender JOIN USAStateGender ON USAGender.id = USAStateGender.date_id;'''
    c.execute(query)
    
    data = c.fetchall()
    
    query = '''SELECT COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths FROM USAGender WHERE AgeGroup = 'All Ages';'''
    c.execute(query)
    all_age_data = c.fetchall()
    usa_all_age = all_age_data[0]
    male_all_age = all_age_data[1]
    female_all_age = all_age_data[2]
    unknown_all_age = all_age_data[3]
    # print(all_age_data)
    
    # calculations of data
    male_percentage = int(round(male_all_age[0] / usa_all_age[0], 2) * 100)
    female_percentage = int(round(female_all_age[0] / usa_all_age[0], 2) * 100)
    unknown_percentage = int(round(unknown_all_age[0] / usa_all_age[0], 2) * 100)
    
    # print(male_percentage)
    # print(female_percentage)
    # print(unknown_percentage)
    
    # finding age groups with each gender
    query = '''SELECT MAX(COVID19Deaths) FROM USAGender WHERE Sex = 'All Sexes' AND AgeGroup <> 'All Ages';'''
    c.execute(query)
    death_count_all = c.fetchone()[0]
    
    query = f'''SELECT AgeGroup FROM USAGender WHERE COVID19Deaths = {death_count_all};'''
    c.execute(query)
    age_group_all = c.fetchone()[0]
    
    # men
    query = '''SELECT MAX(COVID19Deaths) FROM USAGender WHERE Sex = 'Male' AND AgeGroup <> 'All Ages';'''
    c.execute(query)
    death_count_male = c.fetchone()[0]
    
    query = f'''SELECT AgeGroup FROM USAGender WHERE COVID19Deaths = {death_count_male};'''
    c.execute(query)
    age_group_male = c.fetchone()[0]
    
    # female
    query = '''SELECT MAX(COVID19Deaths) FROM USAGender WHERE Sex = 'Female' AND AgeGroup <> 'All Ages';'''
    c.execute(query)
    death_count_female = c.fetchone()[0]

    query = f'''SELECT AgeGroup FROM USAGender WHERE COVID19Deaths = {death_count_female};'''
    c.execute(query)
    age_group_female = c.fetchone()[0]
    
    # find between each gender which illness is more killer
    query = '''SELECT COVID19Deaths, PneumoniaDeaths, InfluenzaDeaths, TotalDeaths FROM USAGender WHERE AgeGroup = 'All Ages';'''
    c.execute(query)
    compare = c.fetchall()
    print(compare)
    all_compare = compare[0]
    male_compare = compare[1]
    female_compare = compare[2]
    unknown_compare = compare[3]
    
    # calculations...
    covid_compare = int(round(all_compare[0] / all_compare[3], 2) * 100)
    pneumonia_compare = int(round(all_compare[1] / all_compare[3], 2) * 100)
    influenza_compare = round(all_compare[2] / all_compare[3], 4) * 100
    
    covid_compare2 = int(round(male_compare[0] / male_compare[3], 2) * 100)
    pneumonia_compare2 = int(round(male_compare[1] / male_compare[3], 2) * 100)
    influenza_compare2 = round(male_compare[2] / male_compare[3], 4) * 100
    
    covid_compare3 = int(round(female_compare[0] / female_compare[3], 2) * 100)
    pneumonia_compare3 = int(round(female_compare[1] / female_compare[3], 2) * 100)
    influenza_compare3 = round(female_compare[2] / female_compare[3], 4) * 100
    
    with open("covid.txt", "a") as file:
        file.write("### USA Gender Data ###\n\n")
        file.write(f"In the US alone, men are dying at alarmingly higher rates than women, accounting for roughly {male_percentage}% of all deaths right now. Women only make up about {female_percentage}%.\n")
        file.write(f"In terms of age group between the genders, the overall most vulnerable group to COVID are ages between {age_group_all}.\n")
        file.write(f"Men however typically die a bit younger with their most vulnerable age group of {age_group_male} taking the most amount of deaths while women are typically more vulnerable around {age_group_female}.\n")
        file.write(f"Furthermore, we decided to compare COVID deaths with deaths of other and similiar conditions that it is consistently compared to, for example Pneumonia and Influenza. For all of America, COVID19 and Pneumonia deaths are roughly equal and account for about {covid_compare}% of all deaths while the flu accounts for only about {influenza_compare}% of all *reported* related deaths thus far this year. Men tend to die from COVID {covid_compare2}% of the time compared to pneumonia and the flu while women tend to die from COVID {covid_compare3}% of the time.")
    

def calculate_countries_gender_data():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    
    query = '''SELECT CountriesGender.Date, CountriesGender.Country, CountriesGender.MaleDeaths, CountriesGender.FemaleDeaths, CountriesGender.TotalDeaths, CountriesAgeSex.AgeGroup, CountriesAgeSex.FemaleDeaths, CountriesAgeSex.MaleDeaths FROM CountriesGender JOIN CountriesAgeSex ON CountriesGender.id = CountriesAgeSex.country_id;'''
    c.execute(query)
    
    data = c.fetchall()
    # print(data)
    
    date = [i[0] for i in data]
    countries = [i[1] for i in data]
    male_deaths = [i[2] for i in data]
    female_deaths = [i[3] for i in data]
    total_deaths = [i[4] for i in data]
    
    while '' in total_deaths:
        total_deaths.remove('')
        
    max_death_count = sorted(total_deaths, reverse=True)[0]
    print(max_death_count)
    
    query = f'''SELECT Country FROM CountriesGender WHERE TotalDeaths = {max_death_count};'''
    c.execute(query)
    country_max_deaths = c.fetchone()[0]
    print(country_max_deaths)
    
    query = f'''SELECT MaleDeaths, FemaleDeaths, TotalDeaths FROM CountriesGender WHERE Country = '{country_max_deaths}';'''
    c.execute(query)
    male_female_deaths = c.fetchone()
    
    male_percentage = int(round(male_female_deaths[0] / male_female_deaths[2], 2) * 100)
    female_percentage = int(round(male_female_deaths[1] / male_female_deaths[2], 2) * 100)
    
    print(female_percentage)
    
    query = f'''SELECT MalePop, FemalePop, TotalPop FROM CountriesGender WHERE Country = '{country_max_deaths}';'''
    c.execute(query)
    pop_data = c.fetchone()
    print(pop_data)
    
    male_pop_percentage = int(round(pop_data[0] / pop_data[2], 2) * 100)
    female_pop_percentage = int(round(pop_data[1] / pop_data[2], 2) * 100)
    
    print(male_pop_percentage)
    print(female_pop_percentage)
    
    # finding age groups
    query = f'''SELECT AgeGroup, FemaleDeaths, MaleDeaths FROM CountriesAgeSex WHERE Country = '{country_max_deaths}';'''
    
    
    with open("covid.txt", "a") as file:
        file.write("\n\n### Global Gender Data ###\n\n")
        file.write("Unfortunately, for a lot of countries, the gender distribution data is not provided. So take this data with a grain of salt.\n")
        file.write(f"In terms of gender data, the highest COVID count providing this data is {country_max_deaths}, besides the United States. There, men account for {male_percentage}% of all COVID deaths so far with females accounting for only {female_percentage}%. That's quite alarming.\n")
        file.write(f"However, strangely enough, women make up the majority of the population at {female_pop_percentage}%, outnumbering men who make up only {male_pop_percentage}%")
