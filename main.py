# Name: Lotoya Willis
# Date: 10/17/2023
# Assignment: 7
# Due Date: 10/15/2023
# About this project: Build a small scale real-world application that uses
# cryptography, network security, and data protection
# Assumptions: Assumes that the user enters most data correctly
# All work below was performed by Lotoya Willis

from flask import Flask, render_template, request, session, flash
import sqlite3 as sql
import os
import HospitalUsersCreateDB
import TestResultsCreateDB
from socket import *
from cryptography.fernet import Fernet

app = Flask(__name__)


# routes to "home"
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        nm = str(session['name']).strip()
        nm = fernet.decrypt(nm).decode()
        return render_template('home.html', name=nm)


# routes to hospital patient form
@app.route('/enternew')
def add_user():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('enternew.html')

# routes to table of hospital users
@app.route('/list')
def list_users():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        con = sql.connect("HospitalUsersDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from Hospital_Users")
        li = []
        row = []
        patients = cur.fetchall();
        for patient in patients:
            user_id = str(patient[0])
            user = str(patient[1])
            age = str(patient[2])
            phone = str(patient[3])
            covid = str(patient[4])
            level = str(patient[5])
            passw = str(patient[6])

            decrypt_user = fernet.decrypt(user).decode()
            decrypt_phone = fernet.decrypt(phone).decode()
            decrypt_passw = fernet.decrypt(passw).decode()

            row.append(user_id)
            row.append(decrypt_user)
            row.append(age)
            row.append(decrypt_phone)
            row.append(covid)
            row.append(level)
            row.append(decrypt_passw)

            row = tuple(row)

            li.append(row)

            row = []

        return render_template("list.html", rows = li)


# routes to table of hospital users
@app.route('/listresults')
def list_results():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        con = sql.connect("HospitalUsersDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()

        name = str(session['name']).strip()

        cur.execute("select * from HOSPITAL_USERS where Name = ?", (name,))
        patient = cur.fetchone()

        current_user_id = str(patient[0])

        con = sql.connect("UserTestResultsDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()

        cur.execute("select * from User_Test_Results")
        li = []
        row = []
        results = cur.fetchall()
        for result in results:
            user_id = str(result[1])
            test = str(result[2])
            test_result = str(result[3])

            decrypt_test = fernet.decrypt(test).decode()
            decrypt_result = fernet.decrypt(test_result).decode()

            if user_id == current_user_id:
                row.append(decrypt_test)
                row.append(decrypt_result)
                row = tuple(row)
                li.append(row)
                row = []

        return render_template("listresults.html", rows = li)


# gets data entered into the hospital patient form and adds to list of
# hospital patients or prints out error messages
#addrec
@app.route('/enternew', methods=['POST','GET'])
def enternew():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            try:
                # creates an empty list called "output"
                output = []
                # tries to request information from the HTML textboxes and
                # checkbox associated with the variables
                nm = request.form.get('Name')
                ag = request.form.get('Age')
                pn = request.form.get('PhoneNum')
                hc = request.form.get('HasCOVID')
                sl = request.form.get('SecurityLevel')
                pw = request.form.get('Password')

                # strips all spaces from the "Name" and "PhoneNum" data
                nm = str(nm).strip()
                pn = str(pn).strip()

                # checks the length of the string, converts it to int, and
                # gives that value to a variable to use later in an if statement
                if (len(ag) != 0):
                    int_ag = int(ag)
                else:
                    int_ag = 0

                # checks the length of the string, converts it to int, and
                # gives that value to a variable to use later in an if statement
                if (len(sl) != 0):
                    int_sl = int(sl)
                else:
                    int_sl = 0

                pw = str(pw).strip()

                # if "HasCOVID" was not checked, it sets "hc" equal to 0
                if hc != "1":
                    hc = "0"

                # if length of variable equals 0, add error message to list of strings
                # called "output"
                if (len(nm) == 0):
                    output.append("You can not enter in an empty name")

                if (len(pn) == 0):
                    output.append("You can not enter in an empty phone number")

                if (int_ag <= 0 or int_ag >= 121):
                    output.append("The Age must be a whole number greater than 0 and less than 121.")

                if (int_sl < 1 or int_sl > 3):
                    output.append("The SecurityRoleLevel must be a numeric between 1 and 3.")

                if (len(pw) == 0):
                    output.append("You can not enter in an empty pwd")

                # if data collected in hospital patient form passes all tests,
                # add it to the list of users
                if ((len(nm) > 0) and (len(pn) > 0) and (int_ag > 0 and int_ag < 121) and (int_sl >= 1 or int_sl <= 3) and (len(pw) > 0)):
                    with sql.connect("HospitalUsersDB.db") as con:
                        cur = con.cursor()
                        user = fernet.encrypt(nm.encode())
                        user = str(user).strip("b\'")
                        phone = fernet.encrypt(pn.encode())
                        phone = str(phone).strip("b\'")
                        passw = fernet.encrypt(pw.encode())
                        passw = str(passw).strip("b\'")
                        cur.execute('SELECT COUNT(*) FROM HOSPITAL_USERS')
                        num = cur.fetchone()
                        num = int(str(num).strip('(,)'))
                        user_id = num + 1
                        cur.execute("INSERT INTO HOSPITAL_USERS (UserId, Name, Age, PhoneNum, HasCOVID, SecurityLevel, Password) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, user, ag, phone, hc, sl, passw))
                        con.commit()
                        output.append("Record successfully added")

            # if the code above fails, add error message to the end of
            # list of strings called "output"
            except:
                output = []
                con.rollback()
                output.append("error in insert operation")

            # runs HTML template that prints out all the error messages
            finally:
                return render_template("result.html", msgs=output)


# addresultrec
@app.route('/enternewresult', methods=['POST','GET'])
def enternewresult():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            try:
                s.connect("localhost", 9999)
                # creates an empty list called "output"
                output = []
                # tries to request information from the HTML textboxes and
                # checkbox associated with the variables
                ui = request.form.get('UserId')
                tn = request.form.get('TestName')
                tr = request.form.get('TestResult')

                # strips all spaces from the "UserId", "TestName", and "Test Result" data
                ui = str(ui).strip()
                tn = str(tn).strip()
                tr = str(tr).strip()

                # checks the length of the string, converts it to int, and
                # gives that value to a variable to use later in an if statement
                if (len(ui) != 0):
                    int_ui = int(ui)
                else:
                    int_ui = 0

                con = sql.connect("HospitalUsersDB.db")
                cur = con.cursor()

                cur.execute('SELECT COUNT(*) FROM HOSPITAL_USERS')
                num = cur.fetchone()
                num = int(str(num).strip('(,)'))

                # if length of variable equals 0, add error message to list of strings
                # called "output"
                if (int_ui <= 0 or int_ui >= num):
                    output.append("The User Id must be a whole number greater than 0 and less than the max amount of records.")

                if (len(tn) == 0):
                    output.append("You can not enter in an empty test name")

                if (len(tr) == 0):
                    output.append("You can not enter in an empty test result")

                print("HIIIIIIIIII")


                # if data collected in hospital patient form passes all tests,
                # add it to the list of users
                if ((int_ui > 0 and int_ui < num) and (len(tn) > 0) and (len(tr) > 0)):
                    msg = ""
                    msg = str(int_ui) + " " + tn + " " + tr
                    msg = fernet.encrypt(msg.encode())
                    msg = str(msg).strip("b\'")

                    # try to send encrypted key and msg through socket
                    sent_key = s.send(key)
                    sent_msg = s.send(msg)

                    output.append("Query Result : Test result successfully sent!")

            # if the code above fails, add error message to the end of
            # list of strings called "output"
            except:
                output = []
                output.append("Query Result : error Error - Test result NOT sent")

            # runs HTML template that prints out all the error messages
            finally:
                return render_template("result.html", msgs=output)



@app.route('/login', methods=['POST'])
def login():
    try:
        # tries to request information from the HTML textboxes
        # associated with the variables
        nm = request.form.get('username')
        pw = request.form.get('password')

        # strips all spaces from the "Name" and "Password" data
        nm = str(nm).strip()
        pw = str(pw).strip()

        with sql.connect("HospitalUsersDB.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            login_user = None
            login_passw = None
            test = None

            # finds the record associated with this username and password
            cur.execute("""select * from HOSPITAL_USERS""", )
            patients = cur.fetchall()
            for patient in patients:
                user = str(patient[1])

                passw = str(patient[6])

                decrypt_user = fernet.decrypt(user).decode()
                decrypt_passw = fernet.decrypt(passw).decode()

                if decrypt_user == nm and decrypt_passw == pw:
                    login_user = user
                    login_passw = passw
                    test = 1

            if (test != None):
                session['name'] = login_user
                cur.execute("""select * from HOSPITAL_USERS where Name = ? and Password = ?""", (login_user, login_passw))

                # stores the security level
                level = cur.fetchone()[5]
                level = str(level).strip()


                # sets the SecurityLevel variable (sl) equal to the string
                # associated with its level
                if level == "1":
                    sl = "1"
                elif level == "2":
                    sl = "2"
                elif level == "3":
                    sl = "3"

                # stores what security level the user has, so
                # it can be used later in the home.html file
                if (sl == "1"):
                    session['Level1'] = True
                    session['Level2'] = False
                    session['Level3'] = False
                elif (sl == "2"):
                    session['Level2'] = True
                    session['Level1'] = False
                    session['Level3'] = False
                else:
                    session['Level3'] = True
                    session['Level1'] = False
                    session['Level2'] = False
                session['logged_in'] = True
            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')

        # if the code above fails, displays an error message
    except:
        con.rollback()
        flash("error in insert operation2")

        # closes sql table
    finally:
        con.close()
    return home()


# Displays a user's information. This is accessible to all users
@app.route('/showuser')
def show_user():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        con = sql.connect("HospitalUsersDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        name = str(session['name']).strip()

        cur.execute("select * from Hospital_Users where Name = ?", (name,))
        patient = cur.fetchone()

        row = []

        #user_id = str(patient[0])
        user = str(patient[1])
        age = str(patient[2])
        phone = str(patient[3])
        covid = str(patient[4])
        level = str(patient[5])
        passw = str(patient[6])

        decrypt_user = fernet.decrypt(user).decode()
        decrypt_phone = fernet.decrypt(phone).decode()
        decrypt_passw = fernet.decrypt(passw).decode()

        #row.append(user_id)
        row.append(decrypt_user)
        row.append(age)
        row.append(decrypt_phone)
        row.append(covid)
        row.append(level)
        row.append(decrypt_passw)

        row = tuple(row)

        return render_template('showUser.html', row=row)


# logs a user out of the site
@app.route('/logout')
def logout():
    session['name'] = ""
    session['Level1'] = False
    session['Level2'] = False
    session['Level3'] = False
    session['logged_in'] = False
    return render_template('login.html')


# "main" function
if __name__ == '__main__':
    app.secret_key = os.urandom(14)

    s = socket(AF_INET, SOCK_STREAM)

    con = sql.connect('HospitalUsersDB.db')
    cur = con.cursor()

    key = Fernet.generate_key()
    fernet = Fernet(key)

    HospitalUsersCreateDB.main(key)
    TestResultsCreateDB.main(key)

    app.run(debug = True)
    con.commit()
    con.close()
