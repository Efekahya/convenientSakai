from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import hashlib
import htmlParserHelper
hostName = "localhost"
serverPort = 8080

cnx = mysql.connector.connect(user='root', password='pass', host='localhost')
cursor = cnx.cursor(buffered=True)
cursor.execute("CREATE DATABASE IF NOT EXISTS efe DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;")
cursor.execute("USE efe")
cursor.execute("CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, loggedIn INT NOT NULL, sakaiUsername VARCHAR(255), SakaiPassword VARCHAR(255),dersIdList VARCHAR(2550), dersNameList TEXT, dersHocaList TEXT, odevList TEXT, duyuruList TEXT, meetingList TEXT)")


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

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            cursor.execute("SELECT id,username,password FROM user WHERE username=%s", (username,))

            if cursor.fetchone() is None:
                self.wfile.write(bytes("{\"status\":\"success\"}", "utf-8"))
                password = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("INSERT INTO user (username, password,loggedIn) VALUES (%s, %s,%s)", (username, password, 0))
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

            cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))

            if cursor.fetchone() is not None:
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
                    htmlParserHelper.calistir(auth)

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


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
