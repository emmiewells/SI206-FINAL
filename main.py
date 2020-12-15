from src import database
from src import calculate
from src import visualizations
import sqlite3


def main():
    """this is the main function for running everything in the project. Follow the instructions in the readme for how to accomplish this.
    """
    while True:
        choice = int()
        print("Hello. What would you like to do?")

        print("1. Create database")
        print("2. Update database")
        print("3. Calculate results")
        print("4. Plot data")
        print("0. Quit program")

        try:
            choice = int(input())
        except ValueError as e:
            print(f"Error: {e}  - please type an integer between 0-4!")
            continue

        if choice == 0:
            print("Goodbye!")
            break
        elif choice == 1:
            print()
            database.create_databases()
            print()
        elif choice == 2:
            track = 0
            while True:
                table = int()
                print("Which table to update?")
                print("1. Global and USA table")
                print("2. USA State table")
                print("3. Gender Countries tables")
                print("0. Quit program")

                conn = sqlite3.connect("covid.db")
                c = conn.cursor()

                try:
                    table = int(input())
                except ValueError as e:
                    print(f"Error: {e}  - please type an integer between 0-4!")
                    continue

                if table == 0:
                    print("Goodbye!")
                    break
                elif table == 1:
                    print("Please do this only once.")

                    query = '''SELECT * FROM Global;'''
                    c.execute(query)
                    count = len(c.fetchall())
                    
                    if count < 1:
                        database.save_global_data()
                        database.save_usa_data()
                    else:
                        print()
                        print("Tables are full!")
                        print()

                elif table == 2:
                    print("Please do this 3 times")

                    query = '''SELECT * FROM States;'''
                    c.execute(query)
                    state_check = len(c.fetchall())
                    if state_check == 56:
                        print()
                        print("Table at max capacity")
                        print()
                    else:
                        database.save_usa_state_data()

                elif table == 3:
                    track += 1
                    print("Please do this at *least* 14 times and at max 20 times")
                    print(f"You've already gone {track} times")
                    print("Please wait...")
                    database.save_country_data()
                    database.save_countries_gender()
                    database.save_usa_gender_data()
                    database.save_usa_state_gender_data()
                    database.save_countries_age_gender()
        elif choice == 3:
            print("Calculating")
            calculate.calculate_countries_gender_data()
        elif choice == 4:
            print("Plotting...")
            visualizations.main()
        else:
            print("Please type a number between 0-4!")
            continue


if __name__ == '__main__':
    main()
