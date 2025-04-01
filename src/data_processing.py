import pandas as pd

def process_spotify_data():

    """Process Spotify data with track-level uniqueness"""
    spotify_df = pd.read_csv("data/raw/spotify_recently_played.csv")
    
    # clean up the track and artist names
    spotify_df["track_name"] = spotify_df["track_name"].str.strip().str.lower()
    spotify_df["artist"] = spotify_df["artist"].str.strip().str.title()
    
    # get unique tracks
    spotify_df = spotify_df.drop_duplicates(subset=["artist", "track_name"])
    
    # process some more data for cleaner format
    spotify_df["release_date"] = pd.to_datetime(spotify_df["release_date"])
    spotify_df = spotify_df.dropna(subset=["release_date"])
    spotify_df["year"] = spotify_df["release_date"].dt.year
    spotify_df["month"] = spotify_df["release_date"].dt.month
    return spotify_df

def process_billboard_data():
    """Process Billboard data with track alignment"""

    billboard_df = pd.read_csv("data/raw/billboard_hot_100_2024.csv")
    
    # clean track artist and song
    billboard_df["song"] = billboard_df["song"].str.strip().str.lower()
    billboard_df["artist"] = billboard_df["artist"].str.strip().str.title()
    
    # process more to cleanup
    billboard_df["weeks_on_chart"] = pd.to_numeric(billboard_df["weeks_on_chart"], errors="coerce").fillna(0)
    return billboard_df

def merge_data(spotify_db, billboard_df):
    """Merge with proper track-level validation"""

    merged_df = pd.merge(
        spotify_db.rename(columns={"track_name": "title"}),
        billboard_df.rename(columns={"song": "title"}),
        on=["artist", "title"],
        how="inner",
        validate="one_to_many"  # 1 Spotify track -> multiple billboard entries
    )

    # temporal features for modeling
    merged_df["days_since_release"] = (pd.to_datetime("2025-03-31") - merged_df["release_date"]).dt.days
    merged_df["release_quarter"] = merged_df["release_date"].dt.quarter

    # success tier based on peak position
    merged_df["success_tier"] = pd.cut(merged_df["peak_position"],
                                       bins=[0, 10, 50, 100],
                                       labels=["Top Hit", "Moderate", "Niche"])

    return merged_df


if __name__ == "__main__":
    # process raw data
    print("Processing Spotify data...")
    spotify_data = process_spotify_data()

    print("Processing Billboard data...")
    billboard_data = process_billboard_data()

    print("Merging Spotify and Billboard data...")
    merged_data = merge_data(spotify_data, billboard_data)

    # save processed data
    merged_data = merged_data.drop_duplicates(subset=['title', 'artist', 'release_date'])
    merged_data.to_csv("data/processed/merged_data.csv", index=False)
    print(f"Processed data saved with {len(merged_data)}")