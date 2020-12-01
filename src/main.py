import database


def main():
    while True:
        print("Hello. What would you like to do?")

        print("1. Create database")
        print("2. Update database")
        print("3. Delete rows")
        print("4. Start over")
        print("6. To debug interface")
        print("0. Quit program")

        choice = int(input())

        if choice == 0:
            print("Goodbye!")
            break
        elif choice == 1:
            print()
            database.create_databases()
            print()
        elif choice == 2:
            print("Which table to update?")
            print("1. Global table")
            print("2. Country table")
            print("3. Gender cases table")
            print("4. Gender death table")
            print("5. Gender total table")
            print("6. USA Gender table")
            print("7. USA State Gender table")
            print("0. Quit program")

            table = int(input())

            if table == 0:
                print("Goodbye!")
                break
            elif table == 1:
                print("Please do this only once.")
                database.save_global_data()
            elif table == 2:
                print("Please do this at *least* 4 times and at max 6 times")
                database.save_country_data()
            elif table == 3:
                database.save_countries_gender_cases()
            elif table == 4:
                database.save_countries_gender_deaths()
            elif table == 5:
                database.save_countries_gender_total()
            elif table == 6:
                database.save_usa_gender_data()
            elif table == 7:
                database.save_usa_state_gender_data()
        elif choice == 3:
            print("What table would you like to delete rows from?")
            table = input()
            print("To what rows do you want to remove?")
            rows = int(input())
            database.delete_rows(table, rows)
        elif choice == 4:
            print("Starting over...")
            database.start_over()


if __name__ == '__main__':
    main()
