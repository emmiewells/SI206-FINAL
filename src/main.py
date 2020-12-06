import database
import calculate

def main():
    while True:
        print("Hello. What would you like to do?")

        print("1. Create database")
        print("2. Update database")
        print("3. Calculate results")
        print("4. Delete rows")
        print("5. Start over")
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
            print("3. Gender Countries table")
            print("4. USA State Gender table")
            print("7. To test")
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
                database.save_usa_data()
            elif table == 3:
                print("Please do this at *least* 4 times and at max 6 times")
                database.save_countries_gender()
                database.save_usa_gender_data()
                database.save_usa_state_data()
                database.save_usa_state_gender_data()
            elif table == 7:
                database.save_countries_age_gender()
        elif choice == 3:
            calculate.main()
        elif choice == 4:
            print("What table would you like to delete rows from?")
            table = input()
            print("To what rows do you want to remove?")
            rows = int(input())
            database.delete_rows(table, rows)
        elif choice == 5:
            print("Starting over...")
            database.start_over()


if __name__ == '__main__':
    main()
