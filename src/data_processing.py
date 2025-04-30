import pandas as pd
import numpy as np

def process_spotify_data():

    """Process Spotify data with track-level uniqueness"""
    spotify_df = pd.read_csv("data/raw/spotify_enriched_from_billboard.csv")
    
    # clean up the track and artist names
    spotify_df["track_name"] = spotify_df["track_name"].str.strip().str.lower()
    spotify_df["artist"] = spotify_df["artist"].str.strip().str.title()
 
    # process some more data for cleaner format
    spotify_df["release_date"] = spotify_df["release_date"].astype(str)
    spotify_df["release_date"] = spotify_df["release_date"].apply(
        lambda x: x if len(x) > 4 else f"{x}-01-01"
    )
    # convert to datetime
    spotify_df["release_date"] = pd.to_datetime(spotify_df["release_date"], errors="coerce")
    # drop bad dates
    spotify_df = spotify_df.dropna(subset=["release_date"])
    # get unique tracks
    spotify_df = spotify_df.drop_duplicates(subset=["artist", "track_name"])
    spotify_df["year"] = spotify_df["release_date"].dt.year
    spotify_df["month"] = spotify_df["release_date"].dt.month
    return spotify_df

def process_billboard_data():
    """Process Billboard data with track alignment"""

    billboard_df = pd.read_csv("data/raw/billboard_hot_100_2022_2025.csv")
    
    # clean track artist and song
    billboard_df["title"] = billboard_df["title"].str.strip().str.lower()
    billboard_df["artist"] = billboard_df["artist"].str.strip().str.title()
    
    # process more to cleanup
    billboard_df["weeks_on_chart"] = pd.to_numeric(billboard_df["weeks_on_chart"], errors="coerce").fillna(0).astype(int)
    billboard_df["rank"] = pd.to_numeric(billboard_df["rank"], errors="coerce").fillna(999).astype(int)
    billboard_df["peak_position"] = pd.to_numeric(billboard_df["peak_position"], errors="coerce").fillna(999).astype(int)

    return billboard_df

def merge_data(spotify_df, billboard_df):
    """Merge with proper track-level validation"""

    spotify_df = spotify_df.rename(columns={"track_name": "title"})

    merged_df = pd.merge(
        spotify_df,
        billboard_df,
        on=["artist", "title"],
        how="inner",
        validate="one_to_many"  # 1 Spotify track -> multiple billboard entries
    )

    merged_df["release_date"] = pd.to_datetime(merged_df["release_date"], errors='coerce')
    # days since release (cap at 10,000)
    merged_df["days_since_release"] = (pd.to_datetime("2025-04-25") - merged_df["release_date"]).dt.days
    merged_df["days_since_release"] = merged_df["days_since_release"].clip(upper=10000)
    # log-transform the capped values
    merged_df["log_days_since_release"] = np.log1p(merged_df["days_since_release"]) # log 1p to avoid log 0

    # success tier based on peak position
    merged_df["success_tier"] = pd.cut(merged_df["rank"],
                                       bins=[0, 10, 50, 100],
                                       labels=["Top Hit", "Moderate", "Niche"])
    
    # tier map
    tier_map = {'Top Hit': 3, 'Moderate': 2, 'Niche': 1}
    merged_df["success_tier_num"] = merged_df["success_tier"].map(tier_map)

    # # ensure weeks_on_chart is numeric and no missing values
    # merged_df['weeks_on_chart'] = pd.to_numeric(merged_df['weeks_on_chart'], errors='coerce')
    # merged_df['weeks_on_chart'] = merged_df['weeks_on_chart'].fillna(0).astype(int)

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
    merged_data.drop_duplicates(subset=['title', 'artist', 'release_date'], inplace=True)
    merged_data.to_csv("data/processed/merged_data.csv", index=False)
    print(f"Processed data saved with {len(merged_data)}")