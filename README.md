# APP9
## Pre-requisites:
1. OrientDB 2.2
1. Python 3.4 <=
1. Virtualenv
1. Gunicorn
## Startup on Windows
1. Start OrientDB with the binary server.bat. This can be accomplished by going to the orientdb home directory and typing **bin\server.bat** at a Windows command prompt. This should result in messages including INFO Listening binary connections on 0.0.0.0:2424 (protocol v.36, socket=default). This is the socket which the python application will communicate with. You can go to your browser with localhost:2480 to see the studio. 
1. Start a new command prompt and navigate to the APP9 folder and activate the virtual environment to ensure APP9 dependencies are contained. Activate with **venv\Scripts\Activate**. This should result in a **(venv)** at the beginning of the command prompt.
1. Install APP9 requirements with **pip install -r requirements.txt**. This will install all the depdencies to run the application.
1. Start the development web service gateway interface server with **python wsgi.py**. This will serve the application and api to the localhost on port 5000.
1. Go to http://127.0.0.1:5000/home for the example appllicationhome screen. The current version has limited functionality with only those operations in the Home menu and Messages currently working.
1. Go to http://127.0.0.1:5000 for the example API Swagger documentation and testing site. 

