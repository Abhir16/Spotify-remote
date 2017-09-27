# Spotify-remote
Remote server allowing multiple users to control music playback of a single host device, without the need to access that device.

For now, create a spotify developer account and generate client id and secret by creating an application. Make sure you add all redirect urls to the application.
Replace the blank string named `CLIENT_ID` AND `CLIENT_SECRET` with your credentials.

# Running Locally

create python virtualenv

`source yourEnvName/bin/activate`

then run:

`pip install -r requirements.txt`

`export FLASK_APP=app.py`

to run local server

`flask run`




