# GetSmart

GetSmart is a platform that can be used to record smartwatch sensor data. It consists of a smartwatch application, which records and transmits data to the server, and a webserver, which stores the data and makes it availeble to download. In this repository you find the source code of both the smartwatch application and the webserver. The smartwatch application is written in kotlin and for the webserver python, html and mysql are used. 

## User manual
### Server setup
The server is built using the Flask web-framework written in Python. The server can be hosted on a
local machine or using a third-party Python web hosting service. The roadmap for both options are
explained below.

#### Server on local machine
1. Download the server files from GitHub:
https://github.com/MarijnSluijs/BAP/tree/main/Server.
2. Create MySQL database to store data. Documentation:
https://www.w3schools.com/python/python_mysql_create_db.asp.
3. Add MySQL database to the flask file flask_app.py on line 20.
4. Run flask_app.py to start server. The server is now accessible on the local network.
5. To access the server from outside the local network, port 80 has to be forwarded on the router.

The server can now be accessed on the local network using the local IP address of the machine. To
access the server from outside the network, the IP address of the router has to be used.

#### Server on third-party web hosting service
1. Download the server files from GitHub:
https://github.com/MarijnSluijs/BAP/tree/main/Server.
2. Import server files to web hosting service.
3. Create MySQL database on web hosting service.
4. Add MySQL database to the flask file flask_app.py. on line 20.
5. Start hosting the server.

The server can now be accessed using the website URL given by the web hosting service. An image
of the website is shown in Figure A.2.

### Smartwatch application setup
The smartwatch application is developed for the smartwatch Samsung Watch 4. To download the
application onto the smartwatch, the following steps need to be done:

1. Download the application from Github:
https://github.com/MarijnSluijs/BAP/tree/main/Smartwatch%20app.
2. Unzip folder and open in Android Studio.
3. Link Samsung Watch 4 to Android Studio using Wifi or Bluetooth. Documentation:
https://developer.android.com/training/wearables/get-started/creating.
4. Add server IP address/URL in the transmitData.kt file on line 28.
5. Click ”Run ’app’” in Android Studio to upload the application to the smartwatch.

The smartwatch application is now ready to be used. After opening the application, a screen is shown
to fill in the user ID. With the user ID, the recording sessions can be distinguished from
other smartwatch users on the server. After filling in the user ID, a screen is shown asking for
permission to access the sensors. For the application to function correctly, permission
to the sensor has to be granted. After granting permission, the home screen is shown.
On this screen the user can specify the type of activity performed in case the researcher wants to
create a training data. Otherwise the user can leave it on ”Recording”, meaning that a dataset will be
recorded without the type of activity specified.

### Recording data
To send data, the smartwatch user has to click on the button ”RECORD” on the home screen. The
data will be sent to the server where it is stored. On the website of the server the active users, user
history and recording sessions are shown. From here the smartwatch wearers can be monitored and
recordings can be downloaded.