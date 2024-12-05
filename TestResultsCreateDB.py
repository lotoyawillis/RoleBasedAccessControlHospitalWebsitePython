# Name: Lotoya Willis
# Date: 09/17/2023
# Assignment: 3
# Due Date: 09/17/2023
# About this project: A python script that creates and manipulates an SQL table
# Assumptions: Assumes the database path is correct
# All work below was performed by Lotoya Willis

import os.path
import sqlite3
from cryptography.fernet import Fernet


def main(key):
    # To find the path for where the database should be placed
    # Inspired by a solution for "Database cannot be found" on StackOverflow

    DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(DIR, "UserTestResultsDB.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    con.execute('''Drop Table USER_TEST_RESULTS''')

    # Saves changes

    con.commit()

    print("UserTestResults table dropped.")

    # Table created

    cur.execute('''CREATE TABLE USER_TEST_RESULTS(
                    TestResultId INTEGER NOT NULL PRIMARY KEY,    
                    UserId INTEGER NOT NULL,              
                    TestName TEXT NOT NULL,               
                    TestResult TEXT NOT NULL);        
                    ''')

    # Saves changes

    con.commit()

    print("UserTestResults Table created.")

    fernet = Fernet(key)

    # user 1
    user_id1 = 1
    result_id1 = 1

    plain_test1 = 'Chicken Pox'
    test1 = fernet.encrypt(plain_test1.encode('utf-8'))
    test1 = str(test1).strip("b\'")

    plain_result1 = 'negative'
    result1 = fernet.encrypt(plain_result1.encode('utf-8'))
    result1 = str(result1).strip("b\'")

    # user 2
    result_id2 = 2

    plain_test2 = 'Flu'
    test2 = fernet.encrypt(plain_test2.encode('utf-8'))
    test2 = str(test2).strip("b\'")

    plain_result2 = 'negative'
    result2 = fernet.encrypt(plain_result2.encode('utf-8'))
    result2 = str(result2).strip("b\'")

    # user 3
    result_id3 = 3

    plain_test3 = 'Purple'
    test3 = fernet.encrypt(plain_test3.encode('utf-8'))
    test3 = str(test3).strip("b\'")

    plain_result3 = 'Pos'
    result3 = fernet.encrypt(plain_result3.encode('utf-8'))
    result3 = str(result3).strip("b\'")

    # user 4
    user_id2 = 2
    result_id4 = 4

    plain_test4 = 'Chicken Pox'
    test4 = fernet.encrypt(plain_test4.encode('utf-8'))
    test4 = str(test4).strip("b\'")

    plain_result4 = 'positive'
    result4 = fernet.encrypt(plain_result4.encode('utf-8'))
    result4 = str(result4).strip("b\'")

    # user 5
    result_id5 = 5

    plain_test5 = 'Flu'
    test5 = fernet.encrypt(plain_test5.encode('utf-8'))
    test5 = str(test5).strip("b\'")

    plain_result5 = 'positive'
    result5 = fernet.encrypt(plain_result5.encode('utf-8'))
    result5 = str(result5).strip("b\'")

    # user 6
    result_id6 = 6

    plain_test6 = 'Purple'
    test6 = fernet.encrypt(plain_test6.encode('utf-8'))
    test6 = str(test6).strip("b\'")

    plain_result6 = 'negative'
    result6 = fernet.encrypt(plain_result6.encode('utf-8'))
    result6 = str(result6).strip("b\'")


    # Fills table with data from "hospital_users," a user defined variable

    user_test_results = [(result_id1, user_id1, test1, result1),
                         (result_id2, user_id1, test2, result2),
                         (result_id3, user_id1, test3, result3),
                         (result_id4, user_id2, test4, result4),
                         (result_id5, user_id2, test5, result5),
                         (result_id6, user_id2, test6, result6)]

    cur.executemany('Insert Into USER_TEST_RESULTS Values(?,?,?,?)', user_test_results)

    # Saves changes

    con.commit()


    # Prints entire table

    for row in cur.execute('SELECT * FROM USER_TEST_RESULTS;'):
        print(row)

    # Closes table

    con.close()

    print("Connection closed.")


if __name__ == '__main__':
    main()

