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

def fetch_spotify_data_from_billboard(billboard_df):
    records = []
    seen = set()

    for _, row in billboard_df.iterrows():
        title = row['title']
        artist = row['artist']
        key = (title.lower(), artist.lower())

        if key in seen:
            continue
        seen.add(key)

        query = f"track:{title} artist:{artist}"
        try:
            results = sp.search(q=query, type='track', limit=1)
            items = results['tracks']['items']
            if items:
                track = items[0]
                records.append({
                    "track_name": track['name'],
                    "artist": track['artists'][0]['name'],
                    "release_date": track['album']['release_date'],
                    "popularity": track['popularity'],
                    "duration_ms": track['duration_ms'],
                    "spotify_id": track['id']
                })
                print(f"Found: {track['name']} by {track['artists'][0]['name']}")
            else:
                print(f"Not found: {title} by {artist}")
        except Exception as e:
            print(f"Error for {title} by {artist}: {e}")
    return pd.DataFrame(records)

if __name__ == "__main__":
    # Fetch Spotify data
    print("Loading Billboard data...")
    billboard_df = fetch_billboard_data_bulk("2022-01-01", "2025-01-01")
    billboard_df.to_csv("data/raw/billboard_hot_100_2022_2025.csv", index=False)

    print("Fetching Spotify data for Billboard songs...")
    spotify_df = fetch_spotify_data_from_billboard(billboard_df)
    spotify_df.to_csv("data/raw/spotify_enriched_from_billboard.csv", index=False)

    print(f"Saved Spotify metadata for {len(spotify_df)} tracks.")