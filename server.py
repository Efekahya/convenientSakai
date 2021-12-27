from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import hashlib
import htmlParserHelper
from uuid import uuid4
import sendMail
import sendJson
hostName = "localhost"
serverPort = 8080

cnx = mysql.connector.connect(user='root', password='pass', host='localhost')
cursor = cnx.cursor(buffered=True)
cursor.execute("CREATE DATABASE IF NOT EXISTS efe DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;")
cursor.execute("USE efe")
cursor.execute("CREATE TABLE IF NOT EXISTS user       (userId INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, loggedIn INT NOT NULL, sakaiUsername VARCHAR(255), sakaiPassword VARCHAR(255),sessionToken VARCHAR(255), passwordToken VARCHAR(255));")
cursor.execute("CREATE TABLE IF NOT EXISTS dersler    (dersId INT AUTO_INCREMENT PRIMARY KEY, userId INT, FOREIGN KEY (userId) REFERENCES user(userId), siteId VARCHAR(255), dersName VARCHAR(255), dersHoca VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS odevler    (odevId INT AUTO_INCREMENT PRIMARY KEY, dersId INT, FOREIGN KEY (dersId) REFERENCES dersler(dersId) , dueTime VARCHAR(255), icerik TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS duyurular  (duyuruId INT AUTO_INCREMENT PRIMARY KEY, dersId INT, FOREIGN KEY (dersId) REFERENCES dersler(dersId), icerik TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS meetingler (meetingId INT AUTO_INCREMENT PRIMARY KEY, dersId INT ,FOREIGN KEY (dersId) REFERENCES dersler(dersId), dueTime VARCHAR(255), available VARCHAR(255), joinLink VARCHAR(255))")


class MyServer(BaseHTTPRequestHandler):

    def do_POST(self):

        if "/registerSakai" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            username = self.path.split("?")[1].split("&")[0].split("=")[1]
            password = self.path.split("?")[1].split("&")[1].split("=")[1]
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            sakaiUsername = self.path.split("?")[1].split("&")[2].split("=")[1]
            sakaiPassword = self.path.split("?")[1].split("&")[3].split("=")[1]
            auth = {"eid": sakaiUsername, "pw": sakaiPassword, "submit": "Giriş"}
            cursor.execute("SELECT loggedIn FROM user WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user[0] == 1:
                if htmlParserHelper.verifyUser(auth):
                    response = {"Login": "Sakai User Added Successfully"}
                    self.wfile.write(bytes(str(response), "utf-8"))
                    cursor.execute("UPDATE user SET sakaiUsername = %s, sakaiPassword = %s WHERE username = %s AND password = %s",
                                   (sakaiUsername, sakaiPassword, username, password))
                    cnx.commit()
                else:
                    response = {"Login": "Sakai User Verification Unsuccessful Please Check Your Credentials"}
                    self.wfile.write(bytes(str(response), "utf-8"))
            else:
                response = {"Login": "You are not logged in"}
                self.wfile.write(bytes(str(response), "utf-8"))

        elif "/register" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            username = self.path.split("?")[1].split("&")[0].split("=")[1]
            password = self.path.split("?")[1].split("&")[1].split("=")[1]
            email = self.path.split("?")[1].split("&")[2].split("=")[1]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            cursor.execute("SELECT username,password FROM user WHERE username=%s", (username,))

            if cursor.fetchone() is None:
                self.wfile.write(bytes("{\"status\":\"success\"}", "utf-8"))
                password = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("INSERT INTO user (username, password,email,loggedIn) VALUES (%s, %s, %s, %s)", (username, password, email, 1))
                cnx.commit()
                # ask for sakai credentials
                # send to sakai

            else:
                self.wfile.write(bytes("{\"status\":\"fail\"}", "utf-8"))

        elif "/login" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            username = self.path.split("?")[1].split("&")[0].split("=")[1]
            password = self.path.split("?")[1].split("&")[1].split("=")[1]
            password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute("SELECT username FROM user WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user is not None:
                print("Login successful")
                cursor.execute("SELECT sakaiUsername, sakaiPassword FROM user WHERE username = %s AND password = %s", (username, password))
                sakaiCred = cursor.fetchone()
                if sakaiCred[0] is None:
                    response = {"Login": "Successful", "SakaiStatus": "Not Registered"}
                    self.wfile.write(bytes(str(response), "utf-8"))
                else:
                    response = {"Login": "Successful", "SakaiStatus": "Registered"}
                    self.wfile.write(bytes(str(response), "utf-8"))
                    # Get data from sakai
                    auth = {"eid": sakaiCred[0], "pw": sakaiCred[1], "submit": "Giriş"}
                    htmlParserHelper.calistir(auth, user[0])

                cursor.execute("UPDATE user SET loggedIn = 1 WHERE username = %s", (username,))
                cnx.commit()
            else:
                print("Wrong username or password")
                response = {"Login": "Unsuccessful"}
                self.wfile.write(bytes(str(response), "utf-8"))

        elif "/logout" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            username = self.path.split("?")[1].split("&")[0].split("=")[1]
            cursor.execute("UPDATE user SET loggedIn = 0 WHERE username = %s", (username,))
            cnx.commit()
            response = {"Logout": "Successful"}
            self.wfile.write(bytes(str(response), "utf-8"))

        elif "/forgotPassword" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            username = self.path.split("?")[1].split("&")[0].split("=")[1]

            cursor.execute("SELECT passwordToken,email FROM user WHERE username = %s", (username, ))
            user = cursor.fetchone()
            if user is not None:
                if user[0] is None:
                    passwordToken = str(uuid4())
                    cursor.execute("UPDATE user SET passwordToken = %s WHERE username = %s", (passwordToken, username))
                    cnx.commit()
                    sendMail.send(user[1], username, passwordToken)
                    response = {"ChangePassword": "An Email Has Been Sent To You"}
                    self.wfile.write(bytes(str(response), "utf-8"))
                else:
                    response = {"ChangePassword": "You Have Already Requested A Password Change"}
                    self.wfile.write(bytes(str(response), "utf-8"))
            else:
                response = {"ChangePassword": "Unsuccessful Check Your Credentials"}
                self.wfile.write(bytes(str(response), "utf-8"))
        elif "/resetPassword" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            username = self.path.split("?")[1].split("&")[0].split("=")[1]
            token = self.path.split("?")[1].split("&")[1].split("=")[1]
            newPassword = self.path.split("?")[1].split("&")[2].split("=")[1]
            newPassword = hashlib.sha256(newPassword.encode()).hexdigest()
            cursor.execute("SELECT passwordToken FROM user WHERE passwordToken = %s", (token,))

            if cursor.fetchone() is not None:

                cursor.execute("UPDATE user SET password = %s, passwordToken = NULL WHERE username = %s", (newPassword, username))
                cnx.commit()
                response = {"ResetPassword": "Successful"}
                self.wfile.write(bytes(str(response), "utf-8"))

            else:
                response = {"ResetPassword": "Unsuccessful Check Your Token"}
                self.wfile.write(bytes(str(response), "utf-8"))
        elif "/getSakai" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            username = self.path.split("?")[1].split("&")[0].split("=")[1]
            password = self.path.split("?")[1].split("&")[1].split("=")[1]
            password = hashlib.sha256(password.encode()).hexdigest()
            request = self.path.split("?")[1].split("&")[2].split("=")[1]
            cursor.execute("SELECT userId, sakaiUsername FROM user WHERE username = %s AND password = %s", (username, password,))
            sakaiCred = cursor.fetchone()
            if sakaiCred[1] is None:
                response = {"SakaiStatus": "Not Registered"}
                self.wfile.write(bytes(str(response), "utf-8"))
            else:
                if request == "dersler":
                   response = sendJson.getDersler(sakaiCred[0], username, password)
                   self.wfile.write(bytes(str(response), "utf-8"))
                elif request == "odevler":
                    response = sendJson.getOdevler(sakaiCred[0], username, password)
                    self.wfile.write(bytes(str(response), "utf-8"))
                elif request == "duyurular":
                    response = sendJson.getDuyurular(sakaiCred[0], username, password)
                    self.wfile.write(bytes(str(response), "utf-8"))
                elif request == "meetingler":
                    response = sendJson.getMeetingler(sakaiCred[0], username, password)
                    self.wfile.write(bytes(str(response), "utf-8"))
                else:
                    response = {"SakaiStatus": "Wrong request"}
                    self.wfile.write(bytes(str(response), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
