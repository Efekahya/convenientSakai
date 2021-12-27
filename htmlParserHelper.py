# from auth import auth
import requests
import json
import os
import time
import threading
from bs4 import BeautifulSoup as soup
import mysql.connector
# Create a file named auth.py and paste this
# auth = {'eid': 'username', 'pw': 'pass', 'submit': 'Giriş'}
# And change 'username' and 'pass' with your credentials
requests.packages.urllib3.disable_warnings()

# Username and password


siteLink = 'https://online.deu.edu.tr'
loginurl = siteLink + '/relogin'


def verifyUser(auth):
    with requests.session() as s:
        senddata = s.post(loginurl, data=auth, verify=False)
        if "şifreniz hatalı" in senddata.text:
            print("Hatalı kullanıcı adı veya şifre")
            return False
        else:
            return True


def calistir(auth, username):
    # Logged in kalmak için tüm işlemleri session içinde yapıyoruz
    with requests.session() as s:
        senddata = s.post(loginurl, data=auth, verify=False)

        def getDersIDAndNames():

            site_url = siteLink + '/portal/favorites/get'
            response = s.get(site_url, verify=False)

            result_json = json.loads(response.text)
            ders_IDs = result_json['favoriteSiteIds']

            ders_Names = []
            hoca_Names = []
            for i in range(len(ders_IDs)):

                site_url = siteLink + '/direct/site/' + ders_IDs[i] + '.json'
                response = s.get(site_url, verify=False)
                result = json.loads(response.text)

                getDersNamesFromJson = result['entityTitle']
                getHocaNamesFromJson = result["props"]["contact-name"]
                ders_Names.append(getDersNamesFromJson)
                hoca_Names.append(getHocaNamesFromJson)

            items = ["dersName", "dersId", "dersHoca"]

            merge = []
            for i in range(len(ders_IDs)):
                merge.append([ders_Names[i], ders_IDs[i], hoca_Names[i]])

            list_json = [dict(zip(items, item)) for item in merge]

            return list_json

        class Ders:
            def __init__(self, name, id, hoca, odev=["Yok"], duyuru=["Yok"], meeting=["Yok"]):
                self.name = name
                self.id = id
                self.hoca = hoca
                self.odev = odev
                self.duyuru = duyuru
                self.meeting = meeting
            # Duyuruları al ve self.duyuru ya kaydet

            def getAnnouncement(self):
                # Dersin json urlsi
                site_URL = "https://online.deu.edu.tr/direct/announcement/site/" + self.id + ".json"
                response = s.get(site_URL, verify=False)

                # Hatalı dosya çıkabiliyor o yüzden try except bloğu kullandım
                try:
                    result = json.loads(response.content)
                    a = result["announcement_collection"]
                except:
                    a = []
                # placeholder olarak kullanıyorum "b" değişkenini nedense direk self.duyuru ya appendlediğimde tüm dersler için değiştiriyor.
                b = []
                for i in range(len(a)):
                    b.append(soup(a[i]["body"], "html.parser").text)
                self.duyuru = b

            def getAssignment(self):

                site_URL = "https://online.deu.edu.tr/direct/assignment/site/" + self.id + ".json"
                response = s.get(site_URL, verify=False)

                if response.status_code == 404:
                    pass
                else:

                    result = json.loads(response.text)
                    a = result["assignment_collection"]
                    if a == []:
                        pass
                    else:
                        ödevlist = []
                        for i in range(len(a)):
                            # Ödev in saatini epoch cinsinden alıp prettify ediyorum.
                            if a[i]["dueTime"]["epochSecond"] + 9000 - time.time() > 0:
                                test = 0
                                getDueTime = a[i]["dueTime"]["epochSecond"] + 9000
                                convertToTuple = time.gmtime(getDueTime)
                                time_string = time.strftime("%d/%m/%Y, %H:%M:%S", convertToTuple)
                                # Ödevin body kısmı
                                odevContent = soup(a[i]["instructions"], "html.parser").text
                                ödevlist.append({"dueTime": time_string, "content": odevContent})
                    if "test" in locals():
                        self.odev = ödevlist

            def getMeetingIdAndJoin(self):

                site_URL = "https://online.deu.edu.tr/direct/bbb-tool.json?siteId=" + self.id
                response = s.get(site_URL, verify=False)
                result = json.loads(response.text)
                a = result["bbb-tool_collection"]
                meetings = []
                for i in range(len(a)):
                    # Eğer toplantının başlama saati 2+ saati geçmişse id sini alma
                    if a[i]["startDate"] is not None:
                        if (int(time.time()) - int(str(a[i]["startDate"])[:-3])) < 100000:
                            test = 0
                            meetingStartDate = a[i]["startDate"] / 1000 + 9000+1800
                            convertToTuple = time.gmtime(meetingStartDate)
                            time_string = time.strftime("%d/%m/%Y, %H:%M:%S", convertToTuple)
                            # Aldığın id ler valid mi ?
                            site_URL = "https://online.deu.edu.tr/direct/bbb-tool/" + \
                                a[i]["id"] + "/joinMeeting"
                            response = s.get(site_URL, verify=False)

                            if "alreadyEnded" in response.text:
                                isMeetingStarted = "Ended"
                            elif "notStarted" in response.text:
                                isMeetingStarted = "Scheculed"
                            else:
                                isMeetingStarted = True
                            meetings.append({"meetingId": a[i]["id"], "meetingStartDate": time_string,
                                            "siteName": self.name, "available": isMeetingStarted, "meetingUrl": site_URL})
                    if "test" in locals():
                        self.meeting = meetings

    # Ders objelerini oluştur.
    ders_list = getDersIDAndNames()
    dersler = []
    for i in range(len(ders_list)):
        dersler.append(Ders(ders_list[i]["dersName"], ders_list[i]
                       ["dersId"], ders_list[i]["dersHoca"]))

    # Threading

    duyurular = [threading.Thread(target=dersler[i].getAnnouncement, args=())
                 for i in range(len(dersler))]
    ödevler = [threading.Thread(target=dersler[i].getAssignment, args=())
               for i in range(len(dersler))]

    meetingler = [threading.Thread(target=dersler[i].getMeetingIdAndJoin, args=())
                  for i in range(len(dersler))]

    for i in range(len(dersler)):
        duyurular[i].start()
        ödevler[i].start()
        meetingler[i].start()
    for i in range(len(dersler)):
        # Threadi bitir
        duyurular[i].join()
        ödevler[i].join()
        meetingler[i].join()

    cnx = mysql.connector.connect(user='root', password='pass', host='localhost')
    cursor = cnx.cursor(buffered=True)
    cursor.execute("USE efe")
    cursor.execute("SELECT userId FROM user WHERE username = %s", (username,))
    userId = cursor.fetchone()[0]

    for i in range(len(dersler)):
        cursor.execute("SELECT COUNT(siteId) FROM dersler WHERE userId = %s AND siteId = %s", (userId, str(dersler[i].id)))
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO dersler (userId, siteId, dersName, dersHoca) VALUES (%s, %s, %s, %s)",
                           (userId, str(dersler[i].id), str(dersler[i].name), str(dersler[i].hoca),))
            lastDersId = cursor.lastrowid

        for j in range(len(dersler[i].odev)):
            h = dersler[i].odev[j]
            if h != "Yok":
                cursor.execute("SELECT dersId FROM dersler WHERE userId = %s AND siteId = %s", (userId, str(dersler[i].id,)))
                dersId = cursor.fetchone()[0]
                cursor.execute("SELECT dersId FROM odevler WHERE dersId = %s AND icerik = %s", (dersId, str(h["content"],)))

                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO odevler (dersId, dueTime, icerik) VALUES (%s, %s, %s)",
                                   (lastDersId, str(h["dueTime"]), str(h["content"]),))

        for j in range(len(dersler[i].duyuru)):
            h = dersler[i].duyuru[j]
            if h != "Yok":
                cursor.execute("SELECT dersId FROM dersler WHERE userId = %s AND siteId = %s", (userId, str(dersler[i].id),))
                dersId = cursor.fetchone()[0]
                cursor.execute("SELECT dersId FROM duyurular WHERE dersId = %s AND icerik = %s", (dersId, str(h),))

                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO duyurular (dersId, icerik) VALUES (%s, %s)", (lastDersId, str(h),))

        for j in range(len(dersler[i].meeting)):
            h = dersler[i].meeting[j]
            if h != "Yok":
                cursor.execute("SELECT dersId FROM dersler WHERE userId = %s AND siteId = %s", (userId, str(dersler[i].id),))
                dersId = cursor.fetchone()[0]
                cursor.execute("SELECT dersId FROM meetingler WHERE dersId = %s AND joinLink = %s", (dersId, str(h["meetingUrl"]),))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO meetingler (dersId, dueTime, available, joinLink) VALUES (%s, %s, %s, %s)",
                                   (lastDersId, str(h["meetingStartDate"]), str(h["available"]), str(h["meetingUrl"]),))
    print("Dersler başarıyla eklendi.")
    cnx.commit()
