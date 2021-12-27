# convenientSakai

# AUTH 

You need to have a mysql server up and running.</br>
</br>
You can change the credentials in the htmlParserHelper.py and server.py files</br>
||</br>
\\/</br>
cnx = mysql.connector.connect(user='root', password='pass', host='localhost')</br>

# USAGE

With POST method you can request: 
http://localhost:8080/register?username=user&password=pass&email=xxxx@gmail.com
http://localhost:8080/login?username=user&password=pass
http://localhost:8080/registerSakai?username=user&password=pass&sakaiUsername=xxxxxxxx@ogr.deu.edu.tr&sakaiPass=pass
http://localhost:8080/logout?username=user&password=pass
http://localhost:8080/forgotPassword?username=user&password=pass

There is also a reset pasword path but it will be send to your email when you send a request to forgotPassword

With POST method you can request from database:
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=dersler
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=odevler
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=duyurular
http://localhost:8080/getSakai?username=xxxx&password=xxxx&request=meetingler

