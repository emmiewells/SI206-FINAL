import sqlite3


def test():
    print("Hello, calculate!")

    conn = sqlite3.connect("covid.db")
    c = conn.cursor()

    query = '''SELECT * FROM Global;'''
    c.execute(query)

    global_data = c.fetchone()

    query = '''SELECT * FROM Countries;'''
    c.execute(query)

    country_data = c.fetchall()
    print(country_data)

    with open("test.txt", "w") as file:
        for i in country_data:
            file.write(f"The country is {i[1]}")


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
        file.write(
            f"The country with the highest COVID case count is {confirmed_country}, with a total case count of {confirmed}, accounting for about {percentage_confirmed}% of all cases in the world.\n\n")

        file.write(
            f"The country with the highest COVID death count is {deaths_country}, with a total death count of {deaths}, accounting for {percentage_death}% of all death.s\n\n")

        file.write(
            f"The country with the highest COVID recovery count is {recovered_country}, with a total recovery count of {recovered}, accounting for {percentage_recovered}% of all recoveries in the world!\n\n")
