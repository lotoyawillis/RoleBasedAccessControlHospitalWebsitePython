import socketserver
import sqlite3 as sql
from cryptography.fernet import Fernet


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # gets the key
        self.key = self.request.recv(1024).strip()

        # gets the encrypted string
        self.msg = self.request.recv(1024).strip()

        key = str(self.key)

        fernet = Fernet(key)

        print("{}    received message  from:".format(self.client_address[0]))
        decrypt = self.msg

        # decrypts message
        decrypt = fernet.decrypt(decrypt).decode()
        print("message: " + decrypt)

        # splits the message by its spaces
        decrypt_list = decrypt.split()

        int_ui = decrypt_list[0]
        int_ui = int(int_ui)
        tn = decrypt_list[1]
        tr = decrypt_list[2]

        # opens HOSPITAL_USERS and gets the number of records
        con = sql.connect("HospitalUsersDB.db")
        cur = con.cursor()

        cur.execute('SELECT COUNT(*) FROM HOSPITAL_USERS')
        num = cur.fetchone()
        num = int(str(num).strip('(,)'))

        if ((int_ui > 0 and int_ui < num) and (len(tn) > 0) and (len(tr) > 0)):
            with sql.connect("UserTestResultsDB.db") as con:
                cur = con.cursor()

                # encrypts test name and result
                test_name = fernet.encrypt(tn.encode())
                test_name = str(test_name).strip("b\'")
                test_result = fernet.encrypt(tr.encode())
                test_result = str(test_result).strip("b\'")

                cur.execute('SELECT COUNT(*) FROM USER_TEST_RESULTS')
                result_num = cur.fetchone()
                result_num = int(str(result_num).strip('(,)'))
                test_id = result_num + 1

                # inserts test record in USERS_TEST_RESULTS
                cur.execute(
                    "INSERT INTO USER_TEST_RESULTS (TestResultId, UserId, TestName, TestResult) VALUES (?, ?, ?, ?)",
                    (test_id, int_ui, test_name, test_result))
                con.commit()
                print("Record successfully added")




if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 9999

        server = socketserver.TCPServer((HOST, PORT), TCPHandler)

        server.serve_forever()
    except server.error as e:
        print("Error:", e)
        exit(1)
    finally:
        server.close()