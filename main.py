import sqlite3
from prettytable import from_db_cursor
import os
import subprocess
import argparse


# function for connection database
def db_connection(db_name):
    if os.path.isfile(db_name):
        try:
            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()
            return connection, cursor
        except sqlite3.Error as error:
            print(format(error))
    else:
        print("Database not found")


# function for SELECT statement in database
def search(query, cursor):
    if not query.lower().startswith("select"):
        cursor.close()
        print("Only SELECT statements are allowed")
    else:
        try:
            result = from_db_cursor(cursor.execute(query))
            cursor.close()
            return result
        except sqlite3.Error as error:
            print(format(error))


def save_result(file_name, result):
    try:
        with open(file_name, "a" if os.path.exists(file_name) else "w") as file:
            file.write(str(result))
    except Exception as error:
        print(format(error))


# function for linux command execute py files and navigate the file system
def linux_commands(command):
    parts = command.split()

    if parts[0].lower() == 'cd':
        try:
            os.chdir(parts[1])
            print(os.getcwd())
        except Exception as error:
            print(format(error))

    elif parts[-1].endswith('.py'):
        try:
            subprocess.run(['python', command])
        except Exception as error:
            print(format(error))
    else:
        print("Invalid command")


# function to execute Python scripts that can manipulate the data
def manipulate_data(query, cursor):
    if not query.lower().startswith("select"):
        cursor.close()
        print("Only SELECT statements are allowed")
    else:
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                print("Table is empty")
            else:
                file = input("Enter script file name: ")
                args = [str(r) for r in result]
                subprocess.run(['python', file] + args)
            cursor.close()
        except sqlite3.Error as error:
            print(format(error))


def main():
    parser = argparse.ArgumentParser(description='command line tool')
    # To execute a Linux command: py main.py -c "cd /home/user/Desktop" / -c file.py
    parser.add_argument('-c', '--command', help='use linux commands "cd .." or execute py files')
    # to search in database: py main.py -d test.db
    parser.add_argument('-d', '--database', help='search in database')
    # to data manipulation: py main.py -m test.db
    parser.add_argument('-m', '--manipulation', help='data manipulation')
    # save results to file: py main.py -d test.db -s
    parser.add_argument('-s', '--save', help='save results to a file', action='store_true')

    args = parser.parse_args()

    if args.command:
        try:
            linux_commands(args.command)
        except Exception:
            print("Error! try again")
    elif args.database:
        try:
            db_name = args.database
            connection, cursor = db_connection(db_name)
            if connection:
                query = input("enter query : ")
                search_results = search(query, cursor)
                print(search_results)
                if args.save:
                    file_name = input("Enter file name to save results : ")
                    save_result(file_name, search_results)
                connection.close()
        except Exception:
            print("Error! try again")
    elif args.manipulation:
        try:
            db_name = args.manipulation
            connection, cursor = db_connection(db_name)
            if connection:
                query = input("enter query : ")
                manipulate_data(query, cursor)
                connection.commit()
                connection.close()
        except Exception:
            print("Error! try again")
    else:
        print("Enter arguments")


if __name__ == '__main__':
    main()
