import sqlite3


def calculate_general_data():
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
