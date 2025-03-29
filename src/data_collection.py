import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import requests
import configparser
from bs4 import BeautifulSoup
import pandas as pd
from billboard_api import fetch_billboard_data

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
# results = sp.current_user_recently_played(limit=10)
# for item in results['items']:
#     track = item['track']
#     print(f"{track['name']} by {track['artists'][0]['name']}")

def fetch_spotify_data():
    results = sp.search(q="year:2023", type="track", limit=50)
    tracks = []
    for item in results["tracks"]["items"]:
        tracks.append({
            "track_name": item["name"],
            "artist": item["artists"][0]["name"],
            "release_date": item["album"]["release_date"],
            "popularity": item["popularity"],
            "duration_ms": item["duration_ms"]
        })
    return pd.DataFrame(tracks)

if __name__ == "__main__":
    # Fetch Spotify data
    spotify_df = fetch_spotify_data()
    print("Spotify Data:")
    print(spotify_df)

    spotify_df.to_csv("data/raw/spotify_recently_played.csv", index=False)

    # Fetch Billboard data
    billboard_df = fetch_billboard_data(date="2025-03-22", range="1-10")
    print("Billboard Data:")
    print(billboard_df)

    billboard_df.to_csv("data/raw/billboard_hot_100.csv", index=False)