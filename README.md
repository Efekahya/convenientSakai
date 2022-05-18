# convenientSakai
There are 4 different versions of this application <br/><br/>
<b>main.py</b> : Simple pyhton script that gathers and parses data from online education system (sakai). There is no user interface for this application it is simply a proof of concept<br/><br/>
<b>expressServer </b>: A fullstack application that utilitizes MERN stack. This version allows multiple users to register and view their announcements, assignments and meetings.<br/><br/>
<b>kivyApp </b>: Kivy mobile app written in python. This version allows multiple users to register and view  their announcements, assignments and meetings.<br/><br/>
<b>webServer </b>: A backend written in python. This version also supports multiple users. <br/> 

# USAGE 
You can choose from 4 different branches and read more about the endpoints available. I'm currently working on "expressServer" branch. I will no longer develop the other branches so the recommended branch is the "expressServer" branch.

# main.py USAGE 


--> This script goes through your favorite sites that you can alter from your university's Sakai website by simply clicking the star icon next to the name of the class. <br/>
--> You need to change the "auth" object's values with your credentials after that you can simply run the program with "python main.py" command. <br/>
--> You can print out the desired data. <br/>
--> This script will send a request to the domain that is provided on the "siteLink" variable so you may want to change that to your university's Sakai domain <br/>
--> This script is written using OOP fundamentals therefore you can easily access any data you want <br/>

Auth line to be changed : auth = {'eid': '1111111111@ogr.deu.edu.tr', 'pw': '12345', 'submit': 'Giriş'} <br/>
siteLink line to be changed : siteLink = 'https://online.deu.edu.tr'


#### AVAILABLE PROPERTIES ####

print(dersler[7].name)<br />
print(dersler[7].duyuru)<br />
print(dersler[7].meeting[0]["content"]<br />
print(dersler[7].meeting[0]["meetingUrl"]

#### PRINT ALL THE CLASS NAMES ####

for i in range(len(dersler)):<br />
  &ensp;&ensp;&ensp;&ensp;print(dersler[i].name)
