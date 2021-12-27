import mysql.connector
import json
cnx = mysql.connector.connect(user='root', password='pass', host='localhost')
cursor = cnx.cursor(buffered=True, dictionary=True)
cursor.execute("USE efe")


def getDersler(userId, username, password):
    cursor.execute("SELECT dersName, dersHoca FROM dersler WHERE userId = %s", (userId,))
    dersler = cursor.fetchall()
    a = json.dumps(dersler)
    return a


def getOdevler(userId, username, password):
    cursor.execute("SELECT dersId,dersName FROM dersler WHERE userId = %s", (userId,))
    dersler = cursor.fetchall()
    odevler = []
    for i in range(len(dersler)):
        cursor.execute("SELECT dueTime,icerik FROM odevler WHERE dersId = %s", (dersler[i]['dersId'],))
        odev = cursor.fetchall()
        for j in range(len(odev)):
            odev[j]["dersName"] = dersler[i]['dersName']
            odevler.append(odev)
    a = json.dumps(odevler)
    return a


def getDuyurular(userId, username, password):
    cursor.execute("SELECT dersId,dersName FROM dersler WHERE userId = %s", (userId,))
    dersler = cursor.fetchall()
    duyurular = []
    for i in range(len(dersler)):
        cursor.execute("SELECT icerik FROM duyurular WHERE dersId = %s", (dersler[i]['dersId'],))
        duyuru = cursor.fetchall()
        for j in range(len(duyuru)):
            duyuru[j]["dersName"] = dersler[i]['dersName']
            duyurular.append(duyuru)
    a = json.dumps(duyurular)
    return a


def getMeetingler(userId, username, password):
    cursor.execute("SELECT dersId,dersName FROM dersler WHERE userId = %s", (userId,))
    dersler = cursor.fetchall()
    meetingler = []
    for i in range(len(dersler)):
        cursor.execute("SELECT dueTime, available, joinLink FROM meetingler WHERE dersId = %s", (dersler[i]['dersId'],))
        meeting = cursor.fetchall()
        for j in range(len(meeting)):
            meeting[j]["dersName"] = dersler[i]['dersName']
            meetingler.append(meeting)

    a = json.dumps(meetingler)
    return a
