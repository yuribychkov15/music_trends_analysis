import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
import configparser
from bs4 import BeautifulSoup
import pandas as pd

# Spotify API setup
# load from config
config = configparser.ConfigParser()
config.read("config.ini")

auth_manager = SpotifyOAuth(
    client_id=config["SPOTIFY"]["CLIENT_ID"], 
    client_secret=config["SPOTIFY"]["CLIENT_SECRET"], 
    redirect_uri=config["SPOTIFY"]["REDIRECT_URI"],
    scope="user-read-recently-played" # example to fetch recently played tracks
    )

sp = spotipy.Spotify(auth_manager=auth_manager)

# fetch recently played tracks
results = sp.current_user_recently_played(limit=10)
for item in results['items']:
    track = item['track']
    print(f"{track['name']} by {track['artists'][0]['name']}")