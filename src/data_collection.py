import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import requests
import configparser
from bs4 import BeautifulSoup
import pandas as pd
from billboard_api import fetch_billboard_data_bulk, fetch_billboard_data

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
    tracks = []
    for offset in range(0, 1000, 50): # fetch up to 200 tracks in batches of 50
        results = sp.search(q="year:2024", type="track", limit=50, offset=offset)
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
    # Billboard Collection (2024 full year)
    print("\nFetching Billboard data...")
    billboard_df = fetch_billboard_data_bulk("2024-01-06", "2024-12-28")  # Saturdays only
    if not billboard_df.empty:
        billboard_df.to_csv("data/raw/billboard_hot_100_2024.csv", index=False)
        print(f"Saved {len(billboard_df)} Billboard chart entries")
    else:
        print("No Billboard data collected")