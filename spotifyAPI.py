from flask import Flask, render_template, request
import requests
from requests.auth import HTTPBasicAuth
import random

app = Flask(__name__, static_folder='statics', template_folder='template93')

def get_spotify_token():
    client_id = "cdf81c2b2fe741dca008ae9963d68e38"
    client_secret = "db460a18445e44d482bbb1ee1b3ba182"
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    auth = HTTPBasicAuth(client_id, client_secret)
    response = requests.post(url, data=data, auth=auth)
    return response.json()["access_token"]

def get_tracks(artist):
    access_token = get_spotify_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.spotify.com/v1/search"
    
    search = f"?q=artist:{artist}&type=track&limit=3"
    full_url = f"{url}{search}"
    
    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        
        tracks = response.json().get("tracks", {}).get("items", [])
        return tracks
    except requests.exceptions.RequestException as e:
        print(f"Error in request: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    artist = request.form.get("artist", "")
    
    tracks = get_tracks(artist) if artist else []
    
    # If no tracks found, provide default tracks
    if not tracks and artist:
        default_tracks = [
            {"name": "Shape of You", "album": {"name": "÷ (Divide)"}, "preview_url": None},
            {"name": "Perfect", "album": {"name": "÷ (Divide)"}, "preview_url": None},
            {"name": "Thinking Out Loud", "album": {"name": "x (Multiply)"}, "preview_url": None}
        ]
        tracks = default_tracks
    
    return render_template("index.html", artist=artist, tracks=tracks)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)