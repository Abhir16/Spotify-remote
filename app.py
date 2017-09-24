from flask import Flask, redirect, render_template, request
import json
import requests
import base64
import urllib
import six


app = Flask(__name__)


# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

#  Client Keys
CLIENT_ID = "" # add client id
CLIENT_SECRET = "" #add client secret

SCOPE = "playlist-modify-public playlist-modify-private"
REDIRECT_URI_PLAY = "http://127.0.0.1:5000/callback/play"
REDIRECT_URI_PAUSE = "http://127.0.0.1:5000/callback/pause"
REDIRECT_URI_NEXT = "http://127.0.0.1:5000/callback/next"
REDIRECT_URI_PREV = "http://127.0.0.1:5000/callback/prev"
REDIRECT_URI_SHUFFLE = "http://127.0.0.1:5000/callback/shuffle"


auth_query_parameters_play = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI_PLAY,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

auth_query_parameters_shuffle = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI_PAUSE,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

auth_query_parameters_next= {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI_NEXT,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

auth_query_parameters_pause= {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI_PREV,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

auth_query_parameters_prev= {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI_SHUFFLE,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

# HELPER METHODS
def createAuthorizationHeaders(client_id, client_secret): # generate auth header for api access
    auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}



#define routes for api calls

@app.route("/")

#prompt user to type spotify credentials
#default to play endpoint, will later use this view to show basic instructions
def home():
	url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters_play.items()])
	auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
	return redirect(auth_url)

@app.route("/play")

def play():
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters_play.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/pause")

def pause():
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters_pause.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/next")

def next():
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters_next.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/prev")

def prev():
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters_prev.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/shuffle")

def shuffle():
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters_shuffle.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


# redirect uris

# MUST BE PREMIUM ACCOUNT FOR THIS FUNCTIONALITY
@app.route("/callback/play")

def playSong():
     #play song
     # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI_PLAY
    }
    headers = createAuthorizationHeaders(CLIENT_ID, CLIENT_SECRET)
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Play current song
    play_request = requests.put("{}/me/player/play".format(SPOTIFY_API_URL), data=code_payload, headers=authorization_header)
    play_response = json.loads(play_request.text)

    # Combine profile and playlist data to display
    display_arr = [play_response]
    return render_template("index.html",sorted_array=display_arr)

@app.route("/callback/pause")

def pauseSong():
     #play song
     # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI_PAUSE
    }
    headers = createAuthorizationHeaders(CLIENT_ID, CLIENT_SECRET)
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Play current song
    play_request = requests.put("{}/me/player/pause".format(SPOTIFY_API_URL), data=code_payload, headers=authorization_header)
    play_response = json.loads(play_request.text)

    # Combine profile and playlist data to display
    display_arr = [play_response]
    return render_template("index.html",sorted_array=display_arr)

@app.route("/callback/next")

def nextSong():
     #play song
     # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI_NEXT
    }
    headers = createAuthorizationHeaders(CLIENT_ID, CLIENT_SECRET)
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Play current song
    play_request = requests.post("{}/me/player/next".format(SPOTIFY_API_URL), data=code_payload, headers=authorization_header)
    play_response = json.loads(play_request.text)

    # Combine profile and playlist data to display
    display_arr = [play_response]
    return render_template("index.html",sorted_array=display_arr)

@app.route("/callback/prev")

def prevSong():
     #play song
     # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI_PREV
    }
    headers = createAuthorizationHeaders(CLIENT_ID, CLIENT_SECRET)
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Play current song
    play_request = requests.post("{}/me/player/previous".format(SPOTIFY_API_URL), data=code_payload, headers=authorization_header)
    play_response = json.loads(play_request.text)

    # Combine profile and playlist data to display
    display_arr = [play_response]
    return render_template("index.html",sorted_array=display_arr)

@app.route("/callback/shuffle")

def shuffleSong():
     #play song
     # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI_SHUFFLE
    }
    headers = createAuthorizationHeaders(CLIENT_ID, CLIENT_SECRET)
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    #add logic to let user set true or false state


    # Play current song
    play_request = requests.put("{}/me/player/shuffle?state=true".format(SPOTIFY_API_URL), data=code_payload, headers=authorization_header)
    play_response = json.loads(play_request.text)

    # Combine profile and playlist data to display
    display_arr = [play_response]
    return render_template("index.html",sorted_array=display_arr)
