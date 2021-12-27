# convenientSakai

# AUTH 

You need to have a mysql server up and running.</br>
</br>
You can change the credentials in the htmlParserHelper.py, sendJson and server.py files</br>
| |</br>
\\/</br>
cnx = mysql.connector.connect(user='root', password='pass', host='localhost')</br>
Also if you want to reset pasword feature to work you need to enter a legit smpt mail to sendMail.json
# USAGE

With POST method you can request: </br>
http://localhost:8080/register?username=user&password=pass&email=xxxx@gmail.com</br>
http://localhost:8080/login?username=user&password=pass</br>
http://localhost:8080/registerSakai?username=user&password=pass&sakaiUsername=xxxxxxxx@ogr.deu.edu.tr&sakaiPass=pass</br>
http://localhost:8080/logout?username=user&password=pass</br>
http://localhost:8080/forgotPassword?username=user&password=pass</br>

There is also a reset pasword path but it will be send to your email when you send a request to forgotPassword

With POST method you can request from database:</br>
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=dersler</br>
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=odevler</br>
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=duyurular</br>
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=meetingler</br>

