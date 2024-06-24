import requests
import base64
from flask import Flask, request, redirect
from urllib.parse import urlencode

app = Flask(__name__)

client_id = "hidden"
client_secret = "hidden"
redirect_uri = "http://localhost:8888/callback"
scope = "playlist-read-private"

@app.route("/")
def authorize():
    url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope
    }
    authorization_url = f"{url}?{urlencode(params)}"
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    if code:
        access_token_data = get_access_token(client_id, client_secret, redirect_uri, code)
        if access_token_data:
            access_token = access_token_data['access_token']
            refresh_token = access_token_data['refresh_token']
            return f"Access Token: {access_token}<br>Refresh Token: {refresh_token}"
        else:
            return "Failed to get access token", 400
    else:
        return "Authorization code not found", 400

def get_access_token(client_id, client_secret, redirect_uri, authorization_code):
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

if __name__ == "__main__":
    app.run(port=8888)
