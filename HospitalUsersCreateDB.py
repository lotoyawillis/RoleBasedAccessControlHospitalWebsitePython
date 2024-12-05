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
    db_path = os.path.join(DIR, "HospitalUsersDB.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    con.execute('''Drop Table Hospital_Users''')

    # Saves changes

    con.commit()

    print("HospitalUser table dropped.")

    # Table created

    cur.execute('''CREATE TABLE HOSPITAL_USERS(
                    UserId INTEGER  NOT NULL PRIMARY KEY,    
                    Name TEXT NOT NULL,              
                    Age TEXT NOT NULL,               
                    PhoneNum TEXT NOT NULL,          
                    HasCOVID TEXT NOT NULL,          
                    SecurityLevel INTEGER NOT NULL,  
                    Password TEXT NOT NULL );        
                    ''')

    # Saves changes

    con.commit()

    print("HospitalUser Table created.")

    fernet = Fernet(key)

    # user 1
    userId1 = 1

    plain_user1 = 'PDiana'
    user1 = fernet.encrypt(plain_user1.encode('utf-8'))
    user1 = str(user1).strip("b\'")

    plain_phone1 = '123-675-7645'
    phone1 = fernet.encrypt(plain_phone1.encode('utf-8'))
    phone1 = str(phone1).strip("b\'")

    # user 2
    userId2 = 2

    plain_user2 = 'TJones'
    user2 = fernet.encrypt(plain_user2.encode('utf-8'))
    user2 = str(user2).strip("b\'")

    plain_phone2 = '895-345-6523'
    phone2 = fernet.encrypt(plain_phone2.encode('utf-8'))
    phone2 = str(phone2).strip("b\'")

    # user 3
    userId3 = 3

    plain_user3 = 'AMath'
    user3 = fernet.encrypt(plain_user3.encode('utf-8'))
    user3 = str(user3).strip("b\'")

    plain_phone3 = '428-197-3967'
    phone3 = fernet.encrypt(plain_phone3.encode('utf-8'))
    phone3 = str(phone3).strip("b\'")

    # user 4
    userId4 = 4

    plain_user4 = 'BSmith'
    user4 = fernet.encrypt(plain_user4.encode('utf-8'))
    user4 = str(user4).strip("b\'")

    plain_phone4 = '239-567-3498'
    phone4 = fernet.encrypt(plain_phone4.encode('utf-8'))
    phone4 = str(phone4).strip("b\'")

    plain_pass = 'test123'
    pwd = fernet.encrypt(plain_pass.encode('utf-8'))
    pwd = str(pwd).strip("b\'")

    # user 5
    userId5 = 5

    plain_user5 = 'LWillis'
    user5 = fernet.encrypt(plain_user5.encode('utf-8'))
    user5 = str(user5).strip("b\'")

    plain_phone5 = '754-000-0000'
    phone5 = fernet.encrypt(plain_phone5.encode('utf-8'))
    phone5 = str(phone5).strip("b\'")

    plain_pass2 = 'password321'
    pwd2 = fernet.encrypt(plain_pass2.encode('utf-8'))
    pwd2 = str(pwd2).strip("b\'")

    # user 6
    userId6 = 6

    plain_user6 = 'KRedwood'
    user6 = fernet.encrypt(plain_user6.encode('utf-8'))
    user6 = str(user6).strip("b\'")

    plain_phone6 = '850-500-3498'
    phone6 = fernet.encrypt(plain_phone6.encode('utf-8'))
    phone6 = str(phone6).strip("b\'")

    plain_pass3 = 'velvet123'
    pwd3 = fernet.encrypt(plain_pass3.encode('utf-8'))
    pwd3 = str(pwd3).strip("b\'")


    # Fills table with data from "hospital_users," a user defined variable

    hospital_users = [(userId1, user1, '34', phone1, '0', 1, pwd),
                      (userId2, user2, '68', phone2, '1', 2, pwd),
                      (userId3, user3, '29', phone3, '0', 3, pwd),
                      (userId4, user4, '37', phone4, '1', 2, pwd),
                      (userId5, user5, '20', phone5, '0', 3, pwd2),
                      (userId6, user6, '21', phone6, '1', 1, pwd3)]

    cur.executemany('Insert Into HOSPITAL_USERS Values(?,?,?,?,?,?,?)', hospital_users)

    # Saves changes

    con.commit()


    # Prints entire table

    for row in cur.execute('SELECT * FROM HOSPITAL_USERS;'):
        print(row)

    # Closes table

    con.close()

    print("Connection closed.")


if __name__ == '__main__':
    main()

